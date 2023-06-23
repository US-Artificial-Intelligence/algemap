from .utils import Template, sample_from, sample_small_int
import random
import tiktoken
from typing import Tuple, List
import math
from functools import reduce


class Factorization(Template):

    def generate(self, n_lcm=10, n_gcd=10) -> List[Tuple[str, dict]]:
        lcm_gens = [self.lcm_generation() for _ in range(n_lcm)]
        gcd_gens = [self.gcd_generation() for _ in range(n_gcd)]

        return [(x, y) for x, y in lcm_gens] + [(x, y) for x, y in gcd_gens]


    def get_metadata(self, txt, kind, tokens):
        metadata = {
            'char_len': len(txt),
            'tokens': tokens,
            'tokenizer': "cl100k_base",
            'tokens_len': len(tokens),
            'data_type': 'factorization',
            'kind': kind
        }
        return metadata

    def gcd_generation(self):
        n = 2 + sample_small_int(dist="exponential")
        nums = [2 + sample_small_int(dist="exponential", dist_args={'c': .01}) for _ in range(n)]
        gcd = self.find_gcd(*nums)
        
        q, a = sample_from("gcd_prefixes")
        delimeter: str = sample_from("seq_delimeters")

        numbers = delimeter.join([str(x) for x in nums])
        gen = f"{q}{numbers}\n{a}{str(gcd)}"

        encoding = tiktoken.get_encoding("cl100k_base")
        tokens = encoding.encode(gen)

        meta = self.get_metadata(gen, "GCD", tokens)

        return gen, meta

    def lcm_generation(self):
        n = 2 + sample_small_int(dist="exponential")
        nums = [2 + sample_small_int(dist="exponential", dist_args={'c': .05}) for _ in range(n)]
        lcm = self.find_lcm(*nums)

        q, a = sample_from("lcm_prefixes")
        delimeter: str = sample_from("seq_delimeters")

        numbers = delimeter.join([str(x) for x in nums])
        gen = f"{q}{numbers}\n{a}{str(lcm)}"
        
        encoding = tiktoken.get_encoding("cl100k_base")
        tokens = encoding.encode(gen)

        meta = self.get_metadata(gen, "LCM", tokens)

        return gen, meta

    def find_gcd(self, *nums):
        return reduce(math.gcd, nums)
    
    def find_lcm(self, *nums):
        def lcm(a, b):
            return abs(a*b) // math.gcd(a, b)

        return reduce(lcm, nums)


