import unittest

import fstatemachine


class TestTransitionsChecker(unittest.TestCase):
    def setUp(self):
        self.states = ['new', 'accepted', 'rejected']
        self.states_with_aliases_list = [(1, 'new'), (2, 'accepted'), (3, 'rejected')]
        self.states_with_aliases_dict = {1: 'new', 2: 'accepted', 3: 'rejected'}

    def test_check_valid_state_changes(self):
        fixture = [
            ('new', 'accepted'),
            ('new', 'rejected'),
            ('rejected', 'accepted'),
        ]

        transitions = {
            'new': ['accepted', 'rejected'],
            'rejected': ['accepted'],
        }

        for current, new in fixture:
            with self.subTest(current=current, new=new):
                checker = fstatemachine.StateMachine(
                    current=current,
                    states=self.states,
                    transitions=transitions
                )
                checker.check(new)

    def test_check_forbidden_state_changes(self):
        fixture = [
            ('rejected', 'new'),
            ('accepted', 'new'),
            ('accepted', 'rejected'),
        ]

        transitions = {
            'new': ['accepted', 'rejected'],
            'rejected': ['accepted'],
        }

        for current, new in fixture:
            with self.subTest(current=current, new=new):
                with self.assertRaises(fstatemachine.WrongTransition) as e:
                    checker = fstatemachine.StateMachine(
                        current=current,
                        states=self.states,
                        transitions=transitions
                    )
                    checker.check(new)
                self.assertEqual(f'from {current} to {new}', str(e.exception))

    def test_check_forbidden_state_changes_when_states_have_aliases(self):
        fixture = [
            (3, 1, 'from rejected to new'),
            (2, 1, 'from accepted to new'),
            (2, 3, 'from accepted to rejected'),
        ]

        transitions = {
            1: [2, 3],
            3: [2],
        }
        states_fixture = [
            ('list', self.states_with_aliases_list),
            ('dict', self.states_with_aliases_dict),
        ]

        for current, new, expected_error in fixture:
            for states_type, states in states_fixture:
                with self.subTest(current=current, new=new, states_type=states_type):
                    with self.assertRaises(fstatemachine.WrongTransition) as e:
                        checker = fstatemachine.StateMachine(
                            current=current,
                            states=states,
                            transitions=transitions
                        )
                        checker.check(new)
                    self.assertEqual(expected_error, str(e.exception))

    def test_check_for_unknown_state(self):
        with self.assertRaises(ValueError) as e:
            checker = fstatemachine.StateMachine(current='new', states=self.states, transitions={})
            checker.check('not_known')
        self.assertEqual('Unknown state: not_known', str(e.exception))

    def test_pass_unknown_state_as_current_on_init(self):
        with self.assertRaises(ValueError) as e:
            fstatemachine.StateMachine(current='not_known', states=self.states, transitions={})
        self.assertEqual('Unknown state: not_known', str(e.exception))

    def test_parse_common_schema(self):
        schema = {
            'new': ['accepted', 'rejected'],
            'rejected': ['accepted'],
        }

        machine = fstatemachine.StateMachine(current='new', states=self.states, transitions=schema)

        self.assertEqual(schema, machine.transitions)

    def test_all_states_literal(self):
        schema = {
            'new': '__all__',
        }

        machine = fstatemachine.StateMachine(current='new', states=self.states, transitions=schema)

        self.assertEqual(['new'], list(machine.transitions))
        self.assertCountEqual(['accepted', 'rejected'], machine.transitions['new'])

    def test_none_is_empty_and_not_used(self):
        schema = {
            'new': None,
        }

        machine = fstatemachine.StateMachine(current='new', states=self.states, transitions=schema)

        self.assertEqual({}, machine.transitions)

    def test_error_on_unknown_states(self):
        schema = {
            'new': ['accepted', 'pending', 'delivered'],
        }

        with self.assertRaises(ValueError) as e:
            fstatemachine.StateMachine(current='new', states=self.states, transitions=schema)

        self.assertEqual('Unknown states: delivered, pending', str(e.exception))
