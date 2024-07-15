import math
from typing import List, Tuple

# vector field normalization or comparative vector analysis in linguistic space 

def vector_magnitude(v: List[float]) -> float:
    return math.sqrt(sum(x * x for x in v))

def normalize_vector(v: List[float]) -> List[float]:
    mag = vector_magnitude(v)
    return [x / mag for x in v] if mag != 0 else v

def vector_dot_product(v1: List[float], v2: List[float]) -> float:
    return sum(a * b for a, b in zip(v1, v2))

class LinguisticVectorField:
    def __init__(self, vectors: List[List[float]]):
        self.vectors = vectors
        self.normalized_vectors = [normalize_vector(v) for v in vectors]

    def field_similarity(self, other_field: 'LinguisticVectorField') -> float:
        """
        Compare this vector field to another using cosine similarity.
        Returns a value between -1 and 1, where 1 indicates perfect similarity.
        """
        if len(self.normalized_vectors) != len(other_field.normalized_vectors):
            raise ValueError("Vector fields must have the same number of vectors")

        similarities = [
            vector_dot_product(v1, v2)
            for v1, v2 in zip(self.normalized_vectors, other_field.normalized_vectors)
        ]
        return sum(similarities) / len(similarities)

    def field_divergence(self) -> float:
        """
        Calculate the divergence of the vector field.
        This could represent how much the field is "spreading out" or "converging".
        """
        # This is a simplified version of divergence
        return sum(sum(v) for v in self.vectors) / len(self.vectors)

class SyntacticalKernel:
    def __init__(self, literal: str, intent: List[float], embedding: List[float], cognitive_trace: Tuple[float, float]):
        self.literal = literal
        self.intent = intent
        self.embedding = embedding
        self.cognitive_trace = cognitive_trace
        self.vector_field = LinguisticVectorField([intent, embedding, list(cognitive_trace)])

    def field_similarity_to(self, other_kernel: 'SyntacticalKernel') -> float:
        return self.vector_field.field_similarity(other_kernel.vector_field)

    def field_divergence(self) -> float:
        return self.vector_field.field_divergence()

def main():
    # Create some example kernels
    kernel1 = SyntacticalKernel("hello", [1, 0, 0], [0.5, 0.5, 0], (1, 0))
    kernel2 = SyntacticalKernel("world", [0, 1, 0], [0, 0.5, 0.5], (0, 1))
    kernel3 = SyntacticalKernel("python", [0, 0, 1], [0.5, 0, 0.5], (0.707, 0.707))

    # Compare vector fields
    similarity_1_2 = kernel1.field_similarity_to(kernel2)
    similarity_1_3 = kernel1.field_similarity_to(kernel3)
    similarity_2_3 = kernel2.field_similarity_to(kernel3)

    print(f"Similarity between kernel1 and kernel2: {similarity_1_2}")
    print(f"Similarity between kernel1 and kernel3: {similarity_1_3}")
    print(f"Similarity between kernel2 and kernel3: {similarity_2_3}")

    # Calculate field divergences
    div1 = kernel1.field_divergence()
    div2 = kernel2.field_divergence()
    div3 = kernel3.field_divergence()

    print(f"Divergence of kernel1 field: {div1}")
    print(f"Divergence of kernel2 field: {div2}")
    print(f"Divergence of kernel3 field: {div3}")

if __name__ == "__main__":
    main()