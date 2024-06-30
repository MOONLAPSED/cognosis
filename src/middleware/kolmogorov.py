# /src/middleware/kolmogorov.py
# a middleware function for dirty and fast but fail-safe kolmogorov quantifications of syntactically meaningful 'work' in the NLP-sense

import zlib
import math
from typing import Union

def estimate_kolmogorov_complexity(text: str) -> float:
    """
    Estimate the Kolmogorov complexity of a given text using compression.
    
    Args:
    text (str): The input text to analyze.
    
    Returns:
    float: An estimate of the Kolmogorov complexity.
    """
    try:
        # Convert text to bytes
        byte_text = text.encode('utf-8')
        
        # Compress the text
        compressed = zlib.compress(byte_text)
        
        # Calculate the compression ratio
        compression_ratio = len(compressed) / len(byte_text)
        
        # Estimate Kolmogorov complexity
        # We use -log2(compression_ratio) as a rough estimate
        kolmogorov_estimate = -math.log2(compression_ratio)
        
        return kolmogorov_estimate
    
    except Exception as e:
        print(f"Error in estimating Kolmogorov complexity: {e}")
        return float('inf')  # Return infinity if calculation fails

def nlp_work_complexity(
    input_text: str, 
    output_text: str
) -> Union[float, tuple]:
    """
    Estimate the complexity of NLP 'work' by comparing input and output texts.
    
    Args:
    input_text (str): The input text before processing.
    output_text (str): The output text after processing.
    
    Returns:
    float or tuple: Estimated complexity of the work done, or a tuple of 
                    (input_complexity, output_complexity) if comparison fails.
    """
    try:
        input_complexity = estimate_kolmogorov_complexity(input_text)
        output_complexity = estimate_kolmogorov_complexity(output_text)
        
        # Calculate the difference in complexity as a measure of 'work' done
        work_complexity = abs(output_complexity - input_complexity)
        
        return work_complexity
    
    except Exception as e:
        print(f"Error in calculating NLP work complexity: {e}")
        return (input_complexity, output_complexity)

# Example middleware function
def kolmogorov_middleware(input_text: str, output_text: str):
    """
    Middleware function to estimate Kolmogorov complexity of NLP work.
    
    Args:
    input_text (str): The input text before processing.
    output_text (str): The output text after processing.
    
    Returns:
    dict: A dictionary containing complexity estimates.
    """
    work_complexity = nlp_work_complexity(input_text, output_text)
    
    return {
        "input_text": input_text,
        "output_text": output_text,
        "complexity_estimate": work_complexity
    }