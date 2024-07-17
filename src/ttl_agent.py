import logging
import random
import asyncio
from typing import Callable, Any, List, Optional, Dict
from dataclasses import dataclass, field

@dataclass
class ExperimentResult:
    input_data: Any
    output_data: Any
    success: bool
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ExperimentAgent:
    ttl: int
    experiment: Callable[[Any], ExperimentResult]
    termination_condition: Callable[[ExperimentResult], bool]
    initial_input: Any
    experiment_log: List[ExperimentResult] = field(default_factory=list)
    retries: int = 3
    retry_delay: float = 1.0
    max_parallel: int = 1

    async def run(self) -> Optional[ExperimentResult]:
        current_input = self.initial_input
        for _ in range(self.ttl):
            tasks = []
            for _ in range(min(self.retries, self.max_parallel)):
                tasks.append(asyncio.create_task(self._run_experiment(current_input)))
            
            results = await asyncio.gather(*tasks)
            success_result = next((r for r in results if r and r.success), None)
            
            if success_result:
                if self.termination_condition(success_result):
                    logging.info(f"Experiment succeeded and met termination condition: {success_result}")
                    return success_result
                current_input = success_result.output_data
            else:
                logging.info("All parallel attempts failed or met termination condition as failure")
                return None

        logging.info("TTL reached without satisfying termination condition.")
        return None

    async def _run_experiment(self, input_data: Any) -> Optional[ExperimentResult]:
        for attempt in range(self.retries):
            try:
                result = self.experiment(input_data)
                self.experiment_log.append(result)
                logging.debug(f"Experiment result: {result}")
                return result
            except Exception as e:
                logging.error(f"Experiment failed on attempt {attempt + 1} with error: {e}")
                if attempt < self.retries - 1:
                    await asyncio.sleep(self.retry_delay)
        return None

    def get_experiment_log(self) -> List[ExperimentResult]:
        return self.experiment_log

@dataclass
class Theory:
    name: str
    hypothesis: Callable[[Any], bool]
    experiment: Callable[[Any], ExperimentResult]

    def test(self, input_data: Any) -> ExperimentResult:
        result = self.experiment(input_data)
        result.metadata['hypothesis_result'] = self.hypothesis(result.output_data)
        return result

@dataclass
class AntiTheory:
    theory: Theory

    def test(self, input_data: Any) -> ExperimentResult:
        result = self.theory.test(input_data)
        result.success = not result.success
        result.metadata['anti_hypothesis_result'] = not result.metadata['hypothesis_result']
        return result

def sample_experiment(input_data: Any) -> ExperimentResult:
    output_data = input_data + random.randint(1, 10)
    success = output_data % 5 != 0
    return ExperimentResult(input_data, output_data, success)

def sample_termination_condition(result: ExperimentResult) -> bool:
    return result.output_data > 50

async def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    sample_theory = Theory(
        name="Divisibility Theory",
        hypothesis=lambda x: x % 5 != 0,
        experiment=sample_experiment
    )

    sample_anti_theory = AntiTheory(sample_theory)

    agent = ExperimentAgent(
        ttl=100,
        experiment=sample_theory.test,
        termination_condition=sample_termination_condition,
        initial_input=0,
        max_parallel=3
    )

    final_result = await agent.run()
    if final_result:
        logging.info(f"Final experiment result: {final_result}")
    else:
        logging.info("Experiment failed or TTL reached without satisfying termination condition.")

    logging.info("Experiment log:")
    for result in agent.get_experiment_log():
        logging.info(f"  {result}")

if __name__ == "__main__":
    asyncio.run(main())