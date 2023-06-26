from lib2to3.pgen2 import token
from templates.simple_arithmetic_wp import SimpleArithmeticWP
from templates.sequences import Sequence
from templates.factorization import Factorization
from templates.step_by_step_arithmetic import StepByStepArithmetic
from templates.boolean import Boolean
import os
import shutil
import json
from functools import reduce
import random


GENERATIONS_FOLDER = "generations"
HF_FOLDER = "huggingface"
BASE_N = 100

# Saves generations into a folder where each generation gets its own text file
# Metadata is stored in one separate file
# Note: specifying a subfolder would delete and remake folder if it already exists
def save_generations(generations, subfolder=None, metadata_filename="metadata.json"):
    path = os.path.join(GENERATIONS_FOLDER)
    if subfolder:
        path = os.path.join(GENERATIONS_FOLDER, subfolder)
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)

    metas = []
    for i in range(len(generations)):
        txt, meta = generations[i]
        file_path = os.path.join(path, f"{i}.txt")
        with open(file_path, "w") as fhand:
            fhand.write(txt)
            if txt[-1] != "\n":
                fhand.write("\n")
        
        if 'id' in meta:
            raise Warning("Key 'id' overwritten in generation metadata.")
        meta['id'] = i
        metas.append(meta)
    with open(os.path.join(path, metadata_filename), "w") as fhand:
        json.dump(metas, fhand)


# Saves all generations in one json file where the text and metadata are combined
def save_to_hf(generations, filename, subfolder=None):
    path = os.path.join(HF_FOLDER)
    if subfolder:
        path = os.path.join(HF_FOLDER, subfolder)
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)

    to_dump = []
    for i, gen in enumerate(generations):
        txt = gen[0]
        meta = gen[1]
        if 'id' in meta:
            raise Warning("Key 'id' overwritten in generation metadata.")
        if 'txt' in meta:
            raise Warning("Key 'txt' overwritten in generation metadata.")
        to_dump.append({**meta, 'txt': txt, 'id': i})

    with open(os.path.join(path, filename), 'w') as fhand:
        json.dump(to_dump, fhand)


# These are the settings used to generate the original dataset:

def make_hf_train():
    fname = "train.json"
    base = BASE_N
    print("\nTrain")
    generations = \
        SimpleArithmeticWP().generate(simple_addition=base, simple_subtraction=base, multi_num=int(base*2.5)) + \
        Sequence().generate(max_sequence_length=10, min_sequence_length=4, n=base, show_rule=True, show_instructions=False, show_rule_after=False) + \
        Sequence().generate(max_sequence_length=10, min_sequence_length=4, n=base, show_rule=True, show_instructions=False, show_rule_after=True) + \
        Sequence().generate(max_sequence_length=12, min_sequence_length=6, n=base, show_rule=True, show_instructions=True, show_rule_after=False) + \
        Sequence().generate(max_sequence_length=12, min_sequence_length=6, n=base, show_rule=True, show_instructions=True, show_rule_after=True) + \
        Sequence().generate(max_sequence_length=10, min_sequence_length=5, n=base, show_rule=False, show_instructions=True) + \
        StepByStepArithmetic().generate(n_add=int(base*2.5), n_sub=int(base*2.5)) + \
        Boolean().generate(n=base*2) + \
        Boolean().generate(n=base*2, prefix="Below is a boolean expression. Following it are legal manipulations of that expression.\n\n") + \
        Factorization().generate(n_lcm=int(base*2.5), n_gcd=int(base*2.5))

    token_dict = {}
    for gen in generations:
        data_type = gen[1]['data_type']
        if data_type in token_dict:
            token_dict[data_type] += gen[1]['tokens_len']
        else:
            token_dict[data_type] = gen[1]['tokens_len']
    print("# of Tokens\n")
    for data_type in token_dict:
        print(f"{data_type}: {token_dict[data_type]}")
    total = sum([token_dict[x] for x in token_dict])
    print(f"\nTotal: {total}")
    save_to_hf(generations, fname)


def make_hf_test():
    fname = "test.json"
    base = BASE_N // 10
    print("\nTest")
    generations = \
        SimpleArithmeticWP().generate(simple_addition=base, simple_subtraction=base, multi_num=int(base*2.5)) + \
        Sequence().generate(max_sequence_length=10, min_sequence_length=4, n=base, show_rule=True, show_instructions=False, show_rule_after=False) + \
        Sequence().generate(max_sequence_length=10, min_sequence_length=4, n=base, show_rule=True, show_instructions=False, show_rule_after=True) + \
        Sequence().generate(max_sequence_length=12, min_sequence_length=6, n=base, show_rule=True, show_instructions=True, show_rule_after=False) + \
        Sequence().generate(max_sequence_length=12, min_sequence_length=6, n=base, show_rule=True, show_instructions=True, show_rule_after=True) + \
        Sequence().generate(max_sequence_length=10, min_sequence_length=5, n=base, show_rule=False, show_instructions=True) + \
        StepByStepArithmetic().generate(n_add=int(base*2.5), n_sub=int(base*2.5)) + \
        Boolean().generate(n=base*2) + \
        Boolean().generate(n=base*2, prefix="Below is a boolean expression. Following it are legal manipulations of that expression.\n\n") + \
        Factorization().generate(n_lcm=int(base*2.5), n_gcd=int(base*2.5))

    token_dict = {}
    for gen in generations:
        data_type = gen[1]['data_type']
        if data_type in token_dict:
            token_dict[data_type] += gen[1]['tokens_len']
        else:
            token_dict[data_type] = gen[1]['tokens_len']
    print("# of Tokens\n")
    for data_type in token_dict:
        print(f"{data_type}: {token_dict[data_type]}")
    total = sum([token_dict[x] for x in token_dict])
    print(f"\nTotal: {total}")
    save_to_hf(generations, fname)


def make_hf_val():
    fname = "validate.json"
    base = BASE_N // 10
    print("\nTest")
    generations = \
        SimpleArithmeticWP().generate(simple_addition=base, simple_subtraction=base, multi_num=int(base*2.5)) + \
        Sequence().generate(max_sequence_length=10, min_sequence_length=4, n=base, show_rule=True, show_instructions=False, show_rule_after=False) + \
        Sequence().generate(max_sequence_length=10, min_sequence_length=4, n=base, show_rule=True, show_instructions=False, show_rule_after=True) + \
        Sequence().generate(max_sequence_length=12, min_sequence_length=6, n=base, show_rule=True, show_instructions=True, show_rule_after=False) + \
        Sequence().generate(max_sequence_length=12, min_sequence_length=6, n=base, show_rule=True, show_instructions=True, show_rule_after=True) + \
        Sequence().generate(max_sequence_length=10, min_sequence_length=5, n=base, show_rule=False, show_instructions=True) + \
        StepByStepArithmetic().generate(n_add=int(base*2.5), n_sub=int(base*2.5)) + \
        Boolean().generate(n=base*2) + \
        Boolean().generate(n=base*2, prefix="Below is a boolean expression. Following it are legal manipulations of that expression.\n\n") + \
        Factorization().generate(n_lcm=int(base*2.5), n_gcd=int(base*2.5))

    token_dict = {}
    for gen in generations:
        data_type = gen[1]['data_type']
        if data_type in token_dict:
            token_dict[data_type] += gen[1]['tokens_len']
        else:
            token_dict[data_type] = gen[1]['tokens_len']
    print("# of Tokens\n")
    for data_type in token_dict:
        print(f"{data_type}: {token_dict[data_type]}")
    total = sum([token_dict[x] for x in token_dict])
    print(f"\nTotal: {total}")
    save_to_hf(generations, fname)


if __name__ == "__main__":
    random.seed(10)  # used in the original generation
    make_hf_train()
    make_hf_test()
    make_hf_val()
