import re
import json


def extract_boxed(text):
    """Extract content from \\boxed{...}, handling nested braces."""
    match = re.search(r'\\boxed\{', text)
    if not match:
        return None
    start = match.end()
    depth = 1
    i = start
    while i < len(text) and depth > 0:
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
        i += 1
    return text[start:i-1] if depth == 0 else None


def parse_roles(text):
    """Extract {name: role} dict from free-form text."""
    pairs = re.findall(r'(\w+)\s+is\s+(?:a\s+)?(knight|knave)', text, re.IGNORECASE)
    return {name: role.lower() for name, role in pairs}


def compute_score(data_source, solution_str, ground_truth, extra_info=None):
    """
    Extract \\boxed content from model output, parse knight/knave assignments,
    and compare against ground truth dict. Returns 1 if correct, 0 otherwise.
    """
    boxed = extract_boxed(solution_str)
    if boxed is None:
        return 0

    pred = parse_roles(boxed)
    if not pred:
        return 0

    # ground_truth is a JSON string from the dataset
    if isinstance(ground_truth, str):
        gt = json.loads(ground_truth)
    else:
        gt = ground_truth
    
    print(f"{pred=} || {gt=}\n")
    return 1 if pred == gt else 0


