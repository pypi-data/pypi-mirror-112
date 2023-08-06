"""
Module for generic states and state ABCs.

Custom states may be defined for etiher Operational or Action states, but should follow the convention for full
functionality.

# Operational states:

- an offline or unavailable state should be indicated by 0
- operational states should be indicated by values 1 or greater
- inoperable or error states should be indicated by values -1 or less

# Action states

- use 0 to represent an inactive state
- use values 1 or greater to indicate active states


# Custom states

Custom states are supported where a enumeration value is an instance of a State subclass. This adds support for
callbacks when a state is switched to.
"""

import logging
from enum import Enum
from typing import Callable, Union, List


state_logger = logging.getLogger('hein_control.states')


class State:
    def __init__(self,
                 value: int,
                 *callbacks: Callable,
                 ):
        """
        Custom state definition with additional support. An integer value must be specified, and callbacks are supported.
        If callbacks are specified for a state, these callbacks will be automatically executed when the state is set.

        :param value: state value
        :param callbacks: callback functions. These functions should take no arguments.
        """
        self.value = value
        self.callbacks = list(callbacks)

    def __str__(self):
        return f'{self.value} ({len(self.callbacks)} callbacks)'

    def __eq__(self, other: Union[int, 'State']):
        if isinstance(other, State):
            return other.value == self.value
        return other == self.value

    def __lt__(self, other: Union[int, 'State']):
        if isinstance(other, State):
            return self.value < other.value
        return self.value < other

    def __gt__(self, other: Union[int, 'State']):
        if isinstance(other, State):
            return self.value > other.value
        return self.value > other

    def __le__(self, other: Union[int, 'State']):
        return self < other or self == other

    def __ge__(self, other: Union[int, 'State']):
        return self > other or self == other

    @property
    def has_callbacks(self) -> bool:
        """whether the State instance has registered callbacks"""
        return len(self.callbacks) > 0

    def register_callbacks(self, *callbacks: Callable):
        """
        Registers the provided callbacks with the State instance. These callbacks will be executed when a Component
        state manager switches to this state.

        :param callbacks: callbacks to register
        """
        for callback in callbacks:
            if callable(callback) is False:
                raise TypeError(f'the provided callback is not callable: {callback}')
            if callback not in self.callbacks:
                state_logger.debug(f'registering {callback} to {self}')
                self.callbacks.append(callback)

    def deregister_callbacks(self, *callbacks: Callable):
        """
        De-registers callbacks from the State. If a callback is not registered with the instance that callbck will be
        ignored.

        :param callbacks: callbacks to remove from the instance
        """
        for callback in callbacks:
            if callback in self.callbacks:
                state_logger.debug(f'removing {callback} from {self}')
                self.callbacks.remove(callback)

    def execute_callbacks(self) -> List:
        """executes any registered callbacks and returns their return values in order"""
        out = []
        for callback in self.callbacks:
            out.append(callback())
        return out


class StateSet(Enum):
    """A pseudo-IntEnum abstract base class which also supports State instances as values"""

    @classmethod
    def _missing_(cls, value):
        """missing hook for the Enum class which supports the State class"""
        for name, state in cls._member_map_.items():
            # match value to state value
            if value == state.value:
                return state
        raise ValueError(f'{value} is not a valid {cls.__name__}')

    def __lt__(self, other: Union[int, 'StateSet']):
        if isinstance(other, StateSet):
            return self.value < other.value
        return self.value < other

    def __gt__(self, other: Union[int, 'StateSet']):
        if isinstance(other, StateSet):
            return self.value > other.value
        return self.value > other

    def __eq__(self, other: Union[int, 'StateSet']):
        if isinstance(other, StateSet):
            return self.value == other.value
        return self.value == other

    def __le__(self, other: Union[int, 'StateSet']):
        return self < other or self == other

    def __ge__(self, other: Union[int, 'StateSet']):
        return self > other or self == other

    @property
    def has_callbacks(self) -> bool:
        """whether the value has callbacks registered"""
        if isinstance(self.value, State):
            return self.value.has_callbacks
        return False

    def register_callbacks(self, *callbacks: Callable):
        """
        Pass through for registering callbacks with the associated State instance. These callbacks will be executed
        when a Component state manager switches to this state.

        :param callbacks: callbacks to register
        """
        if isinstance(self.value, State) is False:
            raise TypeError(f'the {self.__class__.__name__} value is not a State instance')
        self.value.register_callbacks(*callbacks)

    def deregister_callbacks(self, *callbacks: Callable):
        """
        Pass through for de-registering callbacks with the associated State instance.

        :param callbacks: callbacks to remove from the instance
        """
        if isinstance(self.value, State) is False:
            raise TypeError(f'the {self.__class__.__name__} value is not a State instance')
        self.value.deregister_callbacks(*callbacks)

    def execute_callbacks(self) -> List:
        """
        executes any registered callbacks and returns their return values in order. If the value is not a State
        instance, no action will be taken
        """
        if isinstance(self.value, State):
            return self.value.execute_callbacks()


class OperationalState(StateSet):
    """
    operational state tracker for components. By convention, use 0 to indicate offline, negative values for
    error states, and positive values for online states
    """
    ERROR = State(-1)
    OFFLINE = State(0)
    ONLINE = State(1)


class GenericActionState(StateSet):
    """
    Basic action state tracker for component. By convention, use 0 to represent an inactive state for the inactive
    state check decorator to function.
    """
    IDLE = State(0)
    ACTIVE = State(1)



