import unittest

import fstatemachine


class TestTransitionsSchemaParsing(unittest.TestCase):
    def setUp(self):
        self.states = ['new', 'accepted', 'rejected']

    def test_parse_common_schema(self):
        schema = {
            'new': ['accepted', 'rejected'],
            'rejected': ['accepted'],
        }

        parsed = fstatemachine.parse_transitions(self.states, schema)

        self.assertEqual(schema, parsed)

    def test_all_states_literal(self):
        schema = {
            'new': '__all__',
        }

        parsed = fstatemachine.parse_transitions(self.states, schema)

        self.assertEqual(['new'], list(parsed))
        self.assertCountEqual(['accepted', 'rejected'], parsed['new'])

    def test_none_is_empty_and_not_used(self):
        schema = {
            'new': None,
        }

        parsed = fstatemachine.parse_transitions(self.states, schema)

        self.assertEqual({}, parsed)

    def test_error_on_unknown_states(self):
        schema = {
            'new': ['accepted', 'pending', 'delivered'],
        }

        with self.assertRaises(ValueError) as e:
            fstatemachine.parse_transitions(self.states, schema)

        self.assertEqual('Unknown states: delivered, pending', str(e.exception))


class TestTransitionsChecker(unittest.TestCase):
    def setUp(self):
        self.states = ['new', 'accepted', 'rejected']

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

    def test_check_for_unknown_state(self):
        with self.assertRaises(ValueError) as e:
            checker = fstatemachine.StateMachine(current='new', states=self.states, transitions={})
            checker.check('not_known')
        self.assertEqual('Unknown state: not_known', str(e.exception))

    def test_pass_unknown_state_as_current_on_init(self):
        with self.assertRaises(ValueError) as e:
            fstatemachine.StateMachine(current='not_known', states=self.states, transitions={})
        self.assertEqual('Unknown state: not_known', str(e.exception))
