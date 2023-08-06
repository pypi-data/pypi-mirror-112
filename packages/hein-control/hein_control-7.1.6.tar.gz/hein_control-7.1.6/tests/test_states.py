import threading
import time
import unittest
from hein_control.states import (ComponentState, OperationalState, ensure_component_online, ensure_component_inactive,
                                 BadComponentState, GenericActionState, TemporaryCallback)
from hein_control.states.abc import State, StateSet


class CustomActiveState(StateSet):
    IDLE = 0
    ACTIVE = 1
    HYPERACTIVE = 2
    JUMP_JUMP = 3
    BOOGIE_WOOGIE = 4
    # can you tell I have a two year old?


class TestComponent(ComponentState):
    action_states = CustomActiveState

    @ensure_component_online
    def only_run_online(self):
        return

    @ensure_component_inactive
    def only_run_inactive(self):
        return


class TestComponentStates(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.lock = threading.Lock()
        cls.component_one = TestComponent('test_component1', 1)
        cls.component_two = ComponentState('test_component2', 1)
        cls.component_three = ComponentState('test_component3', 1)

    def set_and_check_state(self, component: ComponentState, attribute: str, state: StateSet):
        """generic tester for action and operational state"""
        # test by value
        setattr(component, attribute, state.value)
        self.assertIs(getattr(component, attribute), state)
        # test by name
        setattr(component, attribute, state.name)
        self.assertIs(getattr(component, attribute), state)
        # test name capitalization support
        setattr(component, attribute, state.name.lower())
        self.assertIs(getattr(component, attribute), state)
        # test direct state setting
        setattr(component, attribute, state)
        self.assertIs(getattr(component, attribute), state)

    def set_and_check_operational_state(self, component: ComponentState, state: OperationalState):
        """tests the setting of an operational state by state, value, and name"""
        # test property setting
        self.set_and_check_state(component, 'current_operational_state', state)
        # test method updating
        component.update_operational_state(state)
        self.assertIs(component.current_operational_state, state)

    def set_and_check_action_state(self, component: ComponentState, state: OperationalState):
        """tests the setting of an active state by state, value, and name"""
        # test property setting
        self.set_and_check_state(component, 'current_action_state', state)
        # test method updating
        component.update_action_state(state)
        self.assertIs(component.current_action_state, state)

    def test_component_state_setting(self):
        """tests setting and retrieval of component states"""
        with self.lock:
            for state in OperationalState:
                self.set_and_check_operational_state(self.component_one, state)

    def test_online_only(self):
        """tests the online check decorator functionality"""
        with self.lock:
            try:
                # check that the method runs
                self.component_one.only_run_online()
                # set to offline state
                self.component_one.current_operational_state = 0
                self.assertRaises(BadComponentState, self.component_one.only_run_online)
                # set to error state
                self.component_one.current_operational_state = -1
                self.assertRaises(BadComponentState, self.component_one.only_run_online)
            finally:
                self.component_one.current_operational_state = OperationalState.ONLINE

    def test_component_activity_setting(self):
        """tests the setting of the component activity"""
        with self.lock:
            for state in GenericActionState:
                self.set_and_check_action_state(self.component_two, state)

    def test_custom_activity_setting(self):
        """tests components with custom activity support"""
        with self.lock:
            for state in CustomActiveState:
                self.set_and_check_action_state(self.component_one, state)

    def test_inactive_only(self):
        """tests the inactive-only decorator functionality"""
        with self.lock:
            try:
                # set to active state
                for state in CustomActiveState:
                    self.component_one.current_action_state = state
                    if state == 0:
                        # check that the method runs
                        self.component_one.only_run_inactive()
                    else:
                        self.assertRaises(BadComponentState, self.component_one.only_run_inactive)
            finally:
                self.component_one.current_action_state = 0

    def update_component_state(self, state):
        """sets component one to an error state after 1 second"""
        time.sleep(1)
        self.component_one.current_operational_state = state

    def get_component_state_thread(self, state: int = -1):
        """retrieves a thread which sets the first component to the specified state"""
        return threading.Thread(
            target=self.update_component_state,
            daemon=True,
            args=[state],
        )

    def test_self_waiting(self):
        """tests waiting on a component where the error flag is switched mid-wait"""
        with self.lock:
            try:
                # ensure state monitor actually sleeps
                self.component_one.components_state_monitor_sleep(0.1)
                # tests that error raises
                first_thread = self.get_component_state_thread()
                first_thread.start()
                self.assertRaises(
                    BadComponentState,
                    self.component_one.components_state_monitor_sleep,
                    2
                )

            finally:
                self.component_one.current_operational_state = 1

    def test_adjacent_waiting(self):
        """tests a wait where the error flag is flipped on another component"""
        with self.lock:
            try:
                # ensure state monitor actually sleeps
                self.component_two.components_state_monitor_sleep(0.1)
                # perform wait on another component and ensure that bad state propagates to an error
                second_thread = self.get_component_state_thread()
                second_thread.start()
                self.assertRaises(
                    BadComponentState,
                    self.component_two.components_state_monitor_sleep,
                    2
                )

            finally:
                self.component_one.current_operational_state = 1

    def test_solo_monitor(self):
        """tests a wait where a single component is monitored for an error state (ignores errors from other components"""
        with self.lock:
            try:
                # perform wait on an third component, specifically only monitoring that component
                #   component 1 is still in an error state for this test
                third_thread = self.get_component_state_thread()
                third_thread.start()
                self.component_three.components_state_monitor_sleep(
                    1.5,
                    'test_component3'
                )
            finally:
                self.component_one.current_operational_state = 1

    def test_wait_for_operational(self):
        """tests the functionality for waiting for a component to be operational"""
        with self.lock:
            try:
                # set to offline
                self.component_one.current_operational_state = 0
                thread = self.get_component_state_thread(1)
                thread.start()
                self.component_one.wait_for_component_operational_state(1)
            finally:
                self.component_one.current_operational_state = 1


class TestStates(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.test_state_one = State(1)

    def test_comparisons(self):
        """tests integer state comparisons"""
        self.assertTrue(1 == self.test_state_one, 'check eq')
        self.assertTrue(2 > self.test_state_one, 'check gt')
        self.assertTrue(1 >= self.test_state_one, 'check ge eq')
        self.assertTrue(2 >= self.test_state_one, 'check ge gt')
        self.assertTrue(0 < self.test_state_one, 'check lt')
        self.assertTrue(1 <= self.test_state_one, 'check le eq')
        self.assertTrue(0 <= self.test_state_one, 'check le lt')

    def test_state_comparisons(self):
        """tests comparisons between State classes"""
        self.assertTrue(State(1) == self.test_state_one, 'check eq')
        self.assertTrue(State(2) > self.test_state_one, 'check gt')
        self.assertTrue(State(1) >= self.test_state_one, 'check ge eq')
        self.assertTrue(State(2) >= self.test_state_one, 'check ge gt')
        self.assertTrue(State(0) < self.test_state_one, 'check lt')
        self.assertTrue(State(1) <= self.test_state_one, 'check le eq')
        self.assertTrue(State(0) <= self.test_state_one, 'check le lt')

    def test_callbacks(self):
        """tests state callback de/registration and execution"""
        def banana():
            return 1234

        def melon():
            return 'asdf'

        # test registration
        self.test_state_one.register_callbacks(banana, melon)
        self.assertEqual(len(self.test_state_one.callbacks), 2, "ensure callback was added")
        self.assertTrue(banana in self.test_state_one.callbacks, 'check that method is registered')
        self.assertRaises(TypeError, self.test_state_one.register_callbacks, 1, 'check that non-callables are rejected')

        # test execution
        values = self.test_state_one.execute_callbacks()
        self.assertEqual(len(values), 2, 'check that two returns were captured')
        self.assertEqual(values[0], 1234, 'check that first function value is correct')
        self.assertEqual(values[1], 'asdf', 'check that second function value is correct')

        # test deregistration
        self.test_state_one.deregister_callbacks(banana)
        self.assertEqual(len(self.test_state_one.callbacks), 1, 'ensure callback was removed')
        self.assertFalse(banana in self.test_state_one.callbacks, 'check that method was deregistered')


class FancyOperationalStates(StateSet):
    CRAZY_BAD = State(-9000)
    BAD = State(-1)
    OFFLINE = 0
    GOOD = State(1)


class FancyTestComponent(ComponentState):
    operational_states = FancyOperationalStates

    bad_string = 'omg this super bad thing happened'
    good_string = 'never mind, things are fine'
    no_change = 'no change needed'
    allowable_jump = 'sure, you can do that'

    def __init__(self):
        """a test component which has """
        super(FancyTestComponent, self).__init__('fancy_test_component')
        self.real_bad_thing_happened = False
        self.operational_states.BAD.register_callbacks(self.critical_action)
        self.operational_states.GOOD.register_callbacks(self.restore_functionality)
        self.operational_states.CRAZY_BAD.register_callbacks(self.check_operational_state_jump)
        self.action_states.ACTIVE.register_callbacks(self.check_action_state_jump)

    def critical_action(self):
        """registers that a critical thing has happened"""
        self.real_bad_thing_happened = True
        return self.bad_string

    def restore_functionality(self):
        """restores functionality after a critical thing has happened"""
        if self.current_operational_state > 0:
            return self.no_change
        self.real_bad_thing_happened = False
        return self.good_string

    def check_operational_state_jump(self):
        """will raise an error if the state was already changed"""
        if self.current_operational_state == -9000:
            raise ValueError('this error will occur only if the state is changed before the callbacks are executed')
        return self.allowable_jump

    def check_action_state_jump(self):
        """will raise an error if the state was already changed"""
        if self.current_action_state == 1:
            raise ValueError('this error will occur only if the state is changed before the callbacks are executed')
        return self.allowable_jump


class TestComponentCallbacks(unittest.TestCase):
    """Tests automatic callback execution component state switching"""
    @classmethod
    def setUpClass(cls) -> None:
        cls.component = FancyTestComponent()

    def test_registration(self):
        """ensure actions were registered as expected"""
        self.assertTrue(self.component.critical_action in self.component.operational_states.BAD.value.callbacks)
        self.assertTrue(self.component.restore_functionality in self.component.operational_states.GOOD.value.callbacks)

    def test_callback_functionality(self):
        """tests callback functionality"""
        try:
            # change the operational state to a bad state; ensure callback was executed
            value = self.component.update_operational_state(-1)
            self.assertEqual(value[0], self.component.bad_string, 'ensure return value is captured')
            self.assertTrue(self.component.real_bad_thing_happened, 'ensure callback executed as expected')

            # change the operational state to a good one; ensure callback was executed
            value = self.component.update_operational_state(1)
            self.assertEqual(value[0], self.component.good_string, 'ensure return value is captured')
            self.assertFalse(self.component.real_bad_thing_happened, 'ensure callback executed as expected')

            # test condition check within restor function
            value = self.component.update_operational_state(1)
            self.assertEqual(value[0], self.component.no_change, 'ensure conditional checks work')

            # these will fail if the state is updated before the callbacks are executed
            value = self.component.update_operational_state(-9000)
            self.assertEqual(value[0], self.component.allowable_jump)
            value = self.component.update_action_state(1)
            self.assertEqual(value[0], self.component.allowable_jump)
        finally:
            self.component.update_operational_state(1)
            self.component.update_action_state(0)


class SoManyStates(StateSet):
    SUPER_BAD = State(-10)
    QUITE_BAD = State(-2)
    BAD = State(-1)
    NOT_GREAT = State(0)
    OK = State(1)
    GOOD = State(2)
    GREAT = State(3)
    EXCELLENT = State(10)


class AllTheStates(ComponentState):
    operational_states = SoManyStates


class TestTemporaryCallback(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.component = AllTheStates('so many states')
        cls.lock = threading.Lock()

    @staticmethod
    def custom_callback():
        raise ValueError('oh no the worst thing has happened!')

    def check_assigned(self, fn, threshold=0):
        """performs the appropriate assignment checks depending on the threshold state"""
        for state in self.component.operational_states:
            if state <= threshold:
                self.assertTrue(state.has_callbacks, f'ensure callback was assigned to {state}')
                self.assertTrue(
                    fn in state.value.callbacks,
                    f'ensure correct callback was assigned to {state}'
                )
            else:
                self.assertFalse(state.has_callbacks, 'ensure callback was not assigned to states above threshold')
                self.assertFalse(
                    fn in state.value.callbacks,
                    f'ensure callback was not assigned to {state}'
                )

    def test_default_callback(self):
        """tests setting of the default callback method"""
        with self.lock:
            try:
                with TemporaryCallback(self.component) as tcb:
                    self.assertIsInstance(tcb, TemporaryCallback, 'ensure callback TemporaryCallback instance is returned')
                    self.check_assigned(tcb.callback_capture)
                    self.component.update_operational_state(-1)
                    self.assertTrue(tcb.callback_encountered, 'ensure callback was encountered')
                for state in self.component.operational_states:
                    self.assertFalse(
                        tcb.callback_capture in state.value.callbacks,
                        'ensure callback was removed'
                    )
                    self.assertFalse(state.has_callbacks)
            finally:
                self.component.update_operational_state(1)

    def test_threshold_setting(self):
        """tests that the callback was only applied to states at or below the threshold"""
        with self.lock:
            for threshold_state in self.component.operational_states:
                with TemporaryCallback(self.component, threshold_state=threshold_state) as tcb:
                    self.check_assigned(tcb.callback_capture, threshold_state)

    def test_custom_callback(self):
        """tests custom callback setting"""
        with self.lock:
            try:
                with TemporaryCallback(self.component, callbacks=self.custom_callback) as tcb:
                    self.check_assigned(self.custom_callback)
                    self.assertRaises(ValueError, self.change_state_wait)
                self.assertTrue(tcb.callback_encountered)
                # ensure callback was unassigned after exiting
                for state in self.component.operational_states:
                    self.assertFalse(state.has_callbacks)
                    self.assertFalse(tcb.callback_capture in state.value.callbacks)
            finally:
                self.component.update_operational_state(1)

    def change_state_wait(self):
        """
        waits for some time and changes the component operational state. This should trigger an error if it is executed
        inside a TCB context
        """
        time.sleep(0.1)
        self.component.update_operational_state(-1)
