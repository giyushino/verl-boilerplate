#!/bin/bash
eval "$(conda shell.bash hook)"

conda create -n verl python==3.11 -y
conda activate verl
pip install verl uv
uv pip install vllm --torch-backend=auto
pip install flash-attn --no-build-isolation
