# Algemap

Algemap (**Al**gorithmically **ge**nerated **ma**th **p**roblems) is a dataset of computer-generated, logical text for the purpose of LLM training. Rather than use an LLM to generate the synthetic data, Algemap more straightforwardly substitutes varying numbers, phrasing, and identifiers into pre-specified problem templates.

## Variables

The variables folder contains substitutable words or phrases to insert into problem templates.

### Names

The names file was created by taking the most common baby names of 2022, available [here](https://www.ssa.gov/oact/babynames/limits.html), and running the command `cut -d',' -f1 filename` on it. All of the girls names are listed before the boys names.



