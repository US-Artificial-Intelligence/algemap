from templates.simple_arithmetic_wp import SimpleArithmeticWP
from templates.sequences import Sequence
from templates.factorization import Factorization
import os
import shutil
from templates.utils import sample_small_int
import json


GENERATIONS_FOLDER = "generations"


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


if __name__ == "__main__":
    # x = SimpleArithmeticWP().generate(multi_num=10)
    # x = Sequence().generate()
    x = Factorization().generate()
    save_generations(x, subfolder="testing")
