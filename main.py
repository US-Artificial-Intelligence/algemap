from templates.simple_arithmetic_wp import SimpleArithmeticWP
import os
import shutil

GENERATIONS_FOLDER = "generations"


# Note: specifying a subfolder would delete and remake folder if it already exists
def save_generations(generations, subfolder=None):
    path = os.path.join(GENERATIONS_FOLDER)
    if subfolder:
        path = os.path.join(GENERATIONS_FOLDER, subfolder)
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)

    for i in range(len(generations)):
        file_path = os.path.join(path, f"{i}.txt")
        with open(file_path, "w") as fhand:
            gen = generations[i]
            fhand.write(gen)
            if gen[-1] != "\n":
                fhand.write("\n")


if __name__ == "__main__":
    # x = SimpleArithmeticWP().generate()
    # save_generations(x, )
    from templates.utils import sample_from
    print(sample_from("qa_prefixes")[0])

