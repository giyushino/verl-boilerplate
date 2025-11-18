#conda_env: verl
import os
from datasets import Dataset, load_dataset

import argparse

CURRENT_FILE_PATH = os.path.abspath(__file__)
PROJECT_ROOT = os.path.dirname(CURRENT_FILE_PATH)

if __name__ == '__main__':
    # example code for turing gsm8k into parquet file for verl training

    if not os.path.isdir(os.path.join(PROJECT_ROOT, "datasets")):
        os.makedirs(os.path.join(PROJECT_ROOT, "datasets"))

    dataset_name = "gsm8k"
    dataset_save_path = os.path.join(PROJECT_ROOT, "datasets", dataset_name)

    train_dataset = load_dataset("openai/gsm8k", "main")["train"]
    test_dataset = load_dataset("openai/gsm8k", "main")["test"]
    print(train_dataset[0])

    # Construct a `def make_map_fn(split)` for the corresponding datasets.
    def make_map_fn(split):
        def process_fn(example, idx):
            question = example["question"]
            answer = example["answer"]
            data = {
                "data_source": f"{dataset_name}",
                "prompt": [{
                    "role": "user",
                    "content": question
                }],
                "ability": "math",
                "reward_model": {
                    "style": "rule",
                    "ground_truth": answer
                },
                "extra_info": {
                    'split': split,
                    'index': idx
                }
            }
            return data

        return process_fn

    train_dataset = train_dataset.map(function=make_map_fn('train'), with_indices=True)
    test_dataset = test_dataset.map(function=make_map_fn('test'), with_indices=True)

    train_dataset.to_parquet(os.path.join(dataset_save_path, 'train.parquet'))
    test_dataset.to_parquet(os.path.join(dataset_save_path, 'test.parquet'))
    print(f"datasets saved to {dataset_save_path}")
