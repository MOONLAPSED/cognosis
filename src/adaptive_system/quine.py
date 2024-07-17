import hashlib
import random
import math

def evolving_quine():
    # Core information to be preserved
    core_info = "Black box LLM motility experiment"
    
    # Function to measure entropy
    def measure_entropy(s):
        return -sum(p * math.log2(p) for p in [s.count(c)/len(s) for c in set(s)])
    
    # Function to introduce controlled mutations
    def mutate(s, mutation_rate=0.01):
        return ''.join(c if random.random() > mutation_rate else chr(random.randint(32, 126)) for c in s)
    
    # The quine's code (this will be formatted with the actual code later)
    code = 'def evolving_quine():\n{}\n    return f"{{code}}"\n\nprint(evolving_quine())'
    
    # Measure initial entropy
    initial_entropy = measure_entropy(code)
    
    # Introduce mutations
    mutated_code = mutate(code)
    
    # Measure new entropy
    new_entropy = measure_entropy(mutated_code)
    
    # Calculate hash to track changes
    hash_value = hashlib.md5(mutated_code.encode()).hexdigest()
    
    # Embed measurements and core info in the code
    code = code.format(f'''    # Core information: {core_info}
    import hashlib
    import random
    import math
    
    def measure_entropy(s):
        return -sum(p * math.log2(p) for p in [s.count(c)/len(s) for c in set(s)])
    
    def mutate(s, mutation_rate=0.01):
        return ''.join(c if random.random() > mutation_rate else chr(random.randint(32, 126)) for c in s)
    
    # Entropy measurements:
    # Initial: {initial_entropy:.6f}
    # After mutation: {new_entropy:.6f}
    # Hash: {hash_value}''')
    
    return f"{code}"

print(evolving_quine())