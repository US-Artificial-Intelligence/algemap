# Algemap

Algemap (**Al**gorithmically **ge**nerated **ma**th **p**roblems) is a dataset of computer-generated, logical text for the purpose of LLM training. Rather than use an LLM to generate the synthetic data, Algemap more straightforwardly substitutes varying numbers, phrasing, and identifiers into pre-specified problem templates.

## Usage

If you're just interested in using the dataset, it is available on HuggingFace [here](https://huggingface.co/datasets/US-Artificial-Intelligence/algemap).

For re-generating or changing the data, you can use this repo.

There are two requirements, `tiktoken` (for generating tokens from text) and `datasets`, which is only necessary for testing out the dataset on HuggingFace.

You can use the repo and generate the dataset posted online using:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

## Metadata and Features

Different data types have different feature values. For the hugging face data, every row has at least the following features:

- txt, the plain text
- tokens, the tokenized text
- tokens_len, the number of tokens
- data_type, which kind of data is it (step_by_step_arithmetic, boolean, arithmetic_sequence, factorization, simple_arithmetic_wp)
- tokenizer, which for now is always "cl100k_base"
- char_len, the length of the data in characters

Data-type-specific features include:

- simple_arithmetic_wp: answer_start_char, answer_char_len, word_problem_type: ("addition" or "subtraction")
- arithmetic_sequence: rule, which is a string representing the formula for the sequence
- factorization: kind, which can be GCD or LCM
- step_by_step_arithmetic: kind, which can be "addition" or "subtraction"


## Variables

The variables folder contains substitutable words or phrases to insert into problem templates. The files are txts such that in each row, there are any number of quoted strings. The strings on each row are separated by spaces (split using POSIX rules) and then parsed using JSON.

### Names

The two names files, `boy_names.txt` and `girl_names.txt`, were created by taking the most common baby names of 2022, available [here](https://www.ssa.gov/oact/babynames/limits.html), and running the command `cut -d',' -f1 filename` on it before then separating the boys and girls names and cutting off the names at line 2500.

### Add Verbs

Verbs used to represent the addition of two things in a word problem ("took on", "added", etc.)

### LCM/GCD Prefixes

What appears before the question and answer for LCM/GCD problems

### Noun pairs

The singular and plural of nouns used in word problems

### QA Prefixes

Different forms of "Question:" and "Answer:" that may be used

### Seq Delimeters

Sequence delimeters - for example, "-", "->", or ","

## TODOs

Want to see more features, variables, or data types added? Open a pull request. Some good first pull requests might be:

- Adding more noun pairs to `noun_pairs.txt`
- Increasing the optional variation in boolean sequences
- Code for optionally transforming the boolean statements into English
- Showing step by step factorization
- Step by step multipliation dnd division
