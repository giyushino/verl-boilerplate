import re

def extract_solution(solution_str):
    """
    Extract the answer from \\boxed{} format in the model's response.

    Args:
        output: The model's response text

    Returns:
        The extracted answer or None if not found
    """
    # Pattern to match \boxed{...} with balanced braces
    pattern = r'\\boxed\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}'
    matches = re.findall(pattern, solution_str)

    if matches:
        # Return the last boxed answer (in case there are multiple)
        return matches[-1].strip()
    return None

# the print functions are somewhat useful for debugging
def compute_score(data_source, solution_str, ground_truth, extra_info=None):
    """
    Extract \\boxed content from completion and compare to ground truth, return list of rewards
    """
    solution = extract_solution(solution_str)
     
    #print(f"completion: {solution_str} || extract_solution: {solution} || ground truth: {ground_truth}")
    if str(ground_truth) == solution:
        #print("correct")
        return 1
    #print("incorrect")
    return 0
