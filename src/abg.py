import math

class StateMapper:
    def __init__(self):
        self.state_to_value = {}
        self.value_to_state = {}

    def add_mapping(self, state: str):
        """Map a state to its logarithmic value."""
        value = math.log(len(state) + 1)  # Example transformation
        self.state_to_value[state] = value
        self.value_to_state[value] = state

    def get_value(self, state: str):
        """Get the mapped value for a given state."""
        return self.state_to_value.get(state)

    def get_state(self, value: float):
        """Get the state corresponding to a given value."""
        return self.value_to_state.get(value)

    def verify_bijection(self):
        for state, value in self.state_to_value.items():
            assert self.get_value(state) == value, f"Failed for state {state}"
            assert math.isclose(self.get_value(self.get_state(value)), value, rel_tol=1e-9), f"Failed for value {value}"
        print("Bijection verified for all mappings.")

if __name__ == "__main__":
    mapper = StateMapper()
    
    # Add some mappings
    states = ["alpha", "beta", "gamma"]
    for state in states:
        mapper.add_mapping(state)
    
    # Verify the bijection
    mapper.verify_bijection()

    # Check some mappings
    print("Logarithmic value of 'alpha':", mapper.get_value("alpha"))
    print("State corresponding to value:", mapper.get_state(mapper.get_value("alpha")))
