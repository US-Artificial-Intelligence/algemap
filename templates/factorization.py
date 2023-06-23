from .utils import Template, sample_from, sample_small_int
import random
import tiktoken
from typing import Tuple, List
import math
from functools import reduce


class Factorization(Template):

    def generate(self, *args) -> List[Tuple[str, dict]]:
        self.lcm_generation()

    def gcd_generation(self):
        n = 2 + sample_small_int(dist="exponential")
        nums = [2 + sample_small_int(dist="exponential", dist_args={'c': .01}) for _ in range(n)]
        gcd = self.find_gcd(*nums)
        print(gcd)

    def lcm_generation(self):
        n = 2 + sample_small_int(dist="exponential")
        nums = [2 + sample_small_int(dist="exponential", dist_args={'c': .05}) for _ in range(n)]
        print(nums)
        lcm = self.find_lcm(*nums)
        print(lcm)

    def find_gcd(self, *nums):
        return reduce(math.gcd, nums)
    
    def find_lcm(self, *nums):
        def lcm(a, b):
            return abs(a*b) // math.gcd(a, b)

        return reduce(lcm, nums)


