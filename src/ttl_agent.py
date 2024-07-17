import logging
from typing import Callable, Any, List, Optional
from dataclasses import dataclass, field
import random

@dataclass
class ExperimentResult:
    input_data: Any
    output_data: Any
    success: bool

@dataclass
class ExperimentAgent:
    ttl: int
    experiment: Callable[[Any], ExperimentResult]
    termination_condition: Callable[[ExperimentResult], bool]
    initial_input: Any
    experiment_log: List[ExperimentResult] = field(default_factory=list)
    retries: int = 3

    def run(self) -> Optional[ExperimentResult]:
        current_input = self.initial_input
        for _ in range(self.ttl):
            for attempt in range(self.retries):
                try:
                    result = self.experiment(current_input)
                    self.experiment_log.append(result)
                    logging.debug(f"Experiment result: {result}")
                    if self.termination_condition(result):
                        if result.success:
                            logging.info(f"Experiment succeeded with result: {result}")
                            return result
                        else:
                            logging.info(f"Experiment reached termination condition but marked as failed: {result}")
                            break
                    if not result.success:
                        logging.info(f"Experiment failed with result: {result}")
                        break  # Stop if experiment failed
                    current_input = result.output_data
                    break
                except Exception as e:
                    logging.error(f"Experiment failed on attempt {attempt + 1} with error: {e}")
                    if attempt == self.retries - 1:
                        logging.error("Max retries reached. Terminating experiment.")
                        return None
        
        # If TTL is reached or failed
        logging.info("Experiment failed or TTL reached without satisfying termination condition.")
        return None

def sample_experiment(input_data: Any) -> ExperimentResult:
    # Simulated experiment: add a random number to input_data
    output_data = input_data + random.randint(1, 10)
    success = output_data % 5 != 0  # Arbitrary success condition
    return ExperimentResult(input_data, output_data, success)

def sample_termination_condition(result: ExperimentResult) -> bool:
    return result.output_data > 50  # Terminate if output_data exceeds 50

def main():
    # Configure logging to output to console
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    # Create and run an experiment agent
    agent = ExperimentAgent(
        ttl=100,
        experiment=sample_experiment,
        termination_condition=sample_termination_condition,
        initial_input=0
    )

    final_result = agent.run()
    if final_result:
        logging.info(f"Final experiment result: {final_result}")
    else:
        logging.info("Experiment failed or TTL reached without satisfying termination condition.")

if __name__ == "__main__":
    main()
