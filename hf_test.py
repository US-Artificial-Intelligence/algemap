from datasets import load_dataset
from datasets import get_dataset_split_names

dname = "US-Artificial-Intelligence/algemap"

print(f"Splits: {get_dataset_split_names(dname)}")

dataset = load_dataset(dname, split="train")

print(dataset)