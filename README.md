# Algemap

Algemap (**Al**gorithmically **ge**nerated **ma**th **p**roblems) is a dataset of computer-generated, logical text for the purpose of LLM training. Rather than use an LLM to generate the synthetic data, Algemap more straightforwardly substitutes varying numbers, phrasing, and identifiers into pre-specified problem templates.

## Variables

The variables folder contains substitutable words or phrases to insert into problem templates. The files are txts such that in each row, there are any number of quoted strings. The strings on each row are separated by spaces (split using POSIX rules) and then parsed using JSON.

### Names

The two names files, `boy_names.txt` and `girl_names.txt`, were created by taking the most common baby names of 2022, available [here](https://www.ssa.gov/oact/babynames/limits.html), and running the command `cut -d',' -f1 filename` on it before then separating the boys and girls names and cutting off the names at line 2500.

## Ideas and TODOs

### Data types

### TODO

- Deductive reasoning

### Finished

- Simple arithmetic word problems (+ and -)
- Sequences
- GCD, LCM
- Large arithmetic with steps shown

### Other

- Metadata with generation, specific to data type
- Template language?