from templates.simple_arithmetic_wp import SimpleArithmeticWP
from templates.sequences import Sequence
from templates.factorization import Factorization
from templates.step_by_step_arithmetic import StepByStepArithmetic
from templates.boolean import Boolean
import os
import shutil
import json
from functools import reduce


GENERATIONS_FOLDER = "generations"
HF_FOLDER = "huggingface"

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


if __name__ == "__main__":

    # These are the settings used to generate the original dataset:
    generations = \
        SimpleArithmeticWP().generate(simple_addition=100, simple_subtraction=100, multi_num=100) + \
        Sequence().generate(max_sequence_length=10, min_sequence_length=4, n=100, show_rule=True, show_instructions=False, show_rule_after=False) + \
        Sequence().generate(max_sequence_length=10, min_sequence_length=4, n=100, show_rule=True, show_instructions=False, show_rule_after=True) + \
        Sequence().generate(max_sequence_length=12, min_sequence_length=6, n=100, show_rule=True, show_instructions=True, show_rule_after=False) + \
        Sequence().generate(max_sequence_length=12, min_sequence_length=6, n=100, show_rule=True, show_instructions=True, show_rule_after=True) + \
        Sequence().generate(max_sequence_length=10, min_sequence_length=5, n=100, show_rule=False, show_instructions=True) + \
        StepByStepArithmetic().generate(n_add=250, n_sub=250) + \
        Boolean().generate(n=250) + \
        Boolean().generate(n=250, prefix="Below is a boolean expression. Following it are legal manipulations of that expression.\n\n") + \
        Factorization().generate(n_lcm=100, n_gcd=100)

    tokens_len = sum([x[1]['tokens_len'] for x in generations])
    print(f"Tokens in dataset: {tokens_len}")
    save_to_hf(generations, 'train.json')
