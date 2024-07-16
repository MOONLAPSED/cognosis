# main.py
import asyncio
import argparse
import logging
from pathlib import Path
from src.adaptive_system.morphological_system import AdaptiveMorphologicalSystem

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_arguments():
    parser = argparse.ArgumentParser(description="Cognosis Adaptive Morphological System")
    parser.add_argument('--kb_dir', type=str, default='kb', help="Knowledge base directory")
    parser.add_argument('--output_dir', type=str, default='output', help="Output directory")
    parser.add_argument('--max_memory', type=int, default=1000000, help="Maximum memory for the system")
    return parser.parse_args()

async def main():
    args = parse_arguments()
    setup_logging()

    kb_dir = Path(args.kb_dir)
    output_dir = Path(args.output_dir)
    kb_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)

    system = AdaptiveMorphologicalSystem(str(kb_dir), str(output_dir), args.max_memory)
    await system.initialize()

    tasks = [
        "Analyze the concept of morphological source code",
        "Implement a basic neural network",
        "Optimize database queries for large datasets",
        "Design a user interface for a chat application"
    ]

    await system.run(tasks)

    print("Evolution History:")
    for entry in system.get_evolution_history():
        print(f"{entry['timestamp']}: {entry['message']}")

    await system.visualize_knowledge_graph()

if __name__ == "__main__":
    asyncio.run(main())