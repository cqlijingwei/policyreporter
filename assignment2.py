from typing import Dict, Set, Callable
import unittest

class FiniteStateMachine:
    """
    General finite state class
    """
    def __init__(self, states: Set[str], alphabet: Set[str], initial_state: str, final_states: Set[str], transition_function: Callable[[str, str], str]):
        self.states = states
        self.alphabet = alphabet
        self.current_state = initial_state
        self.final_states = final_states
        self.transition_function = transition_function

    def transition(self, input_symbol: str):
        """
        In terms of input symbol, move state
        :param input_symbol: input symbol
        """
        if input_symbol not in self.alphabet:
            raise ValueError(f"input symbol {input_symbol} not exists in alphabet")
        self.current_state = self.transition_function(self.current_state, input_symbol)

    def is_in_final_state(self) -> bool:
        """
        check if current state is accepted
        :return: is state accepted
        """
        return self.current_state in self.final_states

    def get_current_state(self) -> str:
        """
        get curretn state
        :return: current state
        """
        return self.current_state

def mod_three_fsm_transition(current_state: str, input_symbol: str) -> str:
    """
    mod 3 problem's state move function
    :param current_state: current state
    :param input_symbol: input symbol
    :return: next state
    """
    transitions = {
        'S0': {'0': 'S0', '1': 'S1'},
        'S1': {'0': 'S2', '1': 'S0'},
        'S2': {'0': 'S1', '1': 'S2'},
    }
    return transitions[current_state][input_symbol]

def mod_three(binary_string: str) -> int:
    """
    calculate binary number's mod of 3 
    :param binary_string: binary string
    :return: remainder
    """
    states = {'S0', 'S1', 'S2'}
    alphabet = {'0', '1'}
    initial_state = 'S0'
    final_states = {'S0', 'S1', 'S2'}

    fsm = FiniteStateMachine(states, alphabet, initial_state, final_states, mod_three_fsm_transition)

    for symbol in binary_string:
        fsm.transition(symbol)

    state_to_remainder = {'S0': 0, 'S1': 1, 'S2': 2}
    return state_to_remainder[fsm.get_current_state()]

# sample call
print(mod_three('1101'))  # return: 1
print(mod_three('1110'))  # return: 2
print(mod_three('1111'))  # return: 0

class TestModThreeFSM(unittest.TestCase):
    def test_mod_three(self):
        self.assertEqual(mod_three('1101'), 1)
        self.assertEqual(mod_three('1110'), 2)
        self.assertEqual(mod_three('1111'), 0)

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            mod_three('1102')

if __name__ == '__main__':
    unittest.main()