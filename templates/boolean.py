from .utils import Template, sample_from, sample_small_int
import random
import tiktoken
from typing import Tuple, List, Optional
import math
from functools import reduce

class Boolean(Template):

    def generate(self, *args) -> List[Tuple[str, dict]]:
        x = self.gen_tree()
        moves = self.get_moves(x)
        txt = "\n".join([self.get_str(x) for x in moves])
        return [(txt, {})]

    class Op():
        operation: Optional[str] = None  # "AND", "OR", or "NOT"
        operands: List = []  # len=1 for NOT, len=2 for AND, OR
        def __init__(self, operation, operands) -> None:
            self.operation = operation
            self.operands = operands

    class Leaf():
        value: str = ""
        def __init__(self, value) -> None:
            self.value = value

    def get_str(self, op: Op):
        def rec(x):
            if isinstance(x, self.Leaf):
                return x.value
            else:
                # Op
                if x.operation == 'NOT':
                    return "¬(" + rec(x.operands[0]) + ")"
                elif x.operation == "AND":
                    return "(" + rec(x.operands[0]) + ")" + " ∧ " + "(" + rec(x.operands[1]) + ")"
                elif x.operation == "OR":
                    return "(" + rec(x.operands[0]) + ")" + " ∨ " + "(" + rec(x.operands[1]) + ")"
                else:
                    raise NotImplementedError(f"Operation {x.operation} unrecognized")
                
        return rec(op)
    
    def get_moves(self, x):
        # https://www.mi.mun.ca/users/cchaulk/misc/boolean.htm
        def rec(expr):
            new_forms = [expr]
            if isinstance(expr, self.Op):
                # Check for possible boolean manipulations
                if expr.operation == "AND":
                    op1 = expr.operands[0]
                    op2 = expr.operands[1]
                    # 1a
                    if not isinstance(op1, self.Op) and op1.value == "0":
                        new_forms.append(self.Leaf("0"))
                    if not isinstance(op2, self.Op) and op2.value == "0":
                        new_forms.append(self.Leaf("0"))
                    # 2a
                    if not isinstance(op1, self.Op) and op1.value == "1":
                        new_forms.append(op2)
                    if not isinstance(op2, self.Op) and op2.value == "1":
                        new_forms.append(op1)
                    # 3a
                    if not isinstance(op1, self.Op) and not isinstance(op2, self.Op):
                        if op1.value == op2.value:
                            new_forms.append(op1)
                    return new_forms + \
                            [self.Op(expr.operation, [expr.operands[0], x]) for x in rec(expr.operands[1])] + \
                            [self.Op(expr.operation, [x, expr.operands[1]]) for x in rec(expr.operands[0])]
                elif expr.operation == "OR":
                    # TODO
                    return new_forms
                elif x.operation == "NOT":
                    # TODO
                    return new_forms
                else:
                    raise NotImplementedError(f"Operation {x.operation} unrecognized")
            else:
                return new_forms
        moves = rec(x)

        # Pure GPT-4
        def remove_duplicates(data, func):
            seen = {}
            result = []
            for item in data:
                # Apply the function to the item.
                key = func(item)
                # If the key hasn't been seen yet, add the item to the result list.
                if key not in seen:
                    result.append(item)
                    seen[key] = True
            return result
        
        moves = remove_duplicates(moves, self.get_str)
        return moves
    
    def gen_tree(self):
        return self.Op("AND", [self.Op("AND", [self.Leaf("A"), self.Leaf("1")]), self.Leaf("A")])
