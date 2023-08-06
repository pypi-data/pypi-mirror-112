from typing import Dict, Hashable, Iterable, List, Union

__version__ = '1.0.0'


class WrongTransition(Exception):
    """Wrong Transition Error class"""


empty = object()

Transitions = Dict[Hashable, List[Hashable]]


class StateMachine:
    """
    StateMachine class

    :param current: initial state of machine
    :param states: list of available states
    :param transitions: transitions between states
        where key is initial state and value is list of legit states for transition.
        State can be any hashable object.
        It will be convenient if the status implements `__str__` method.

        Value can be:
            - list of states for transition
            - None or empty list for prohibition of transition (or not set key)
            - "__all__" string for specify that any state are available for transition
    :raises: :py:exc:`ValueError`
    """

    def __init__(self, *, current: Hashable, states: Iterable, transitions: Transitions):
        self.states = list(states)
        self.transitions = parse_transitions(self.states, transitions)
        self.current = current

    @property
    def current(self):
        """
        Current state of machine
        """
        return getattr(self, '_current', empty)

    @current.setter
    def current(self, value):
        self.check(value)
        self._current = value

    def check(self, new):
        """
        Check if new state is valid transitions for machine

        :param new: state for check
        :raises: :py:exc:`WrongTransition`, :py:exc:`ValueError`
        """
        if new not in self.states:
            raise ValueError(f'Unknown state: {new}')

        if self.current is empty or self.current == new:
            return

        if new not in self.transitions.get(self.current, []):
            raise WrongTransition(f'from {self.current} to {new}')


Schema = Dict[Hashable, List[Union[Hashable, str, None]]]


def parse_transitions(states: list, transitions_schema: Schema) -> Transitions:
    """
    Parse transitions from transitions schema. Example:
    {
        'new': '__all__',  # literal for specify all states
        'rejected': ['accepted', 'cancelled'],
        'accepted': None  # [] or not set key is the same
    }

    :param states: list of available states
    :param transitions_schema: dict of transitions between states
    :raises: ValueError
    """
    transitions = {}
    known_states = set(states)
    for from_state, to_states in transitions_schema.items():
        if to_states == '__all__':
            to_states = list(known_states - {from_state})
        elif not to_states:
            continue
        else:
            unknown = set(to_states) - known_states
            if unknown:
                states = sorted(str(item) for item in unknown)
                raise ValueError(f'Unknown states: {", ".join(states)}')
        transitions[from_state] = to_states
    return transitions
