from .utils import Template, sample_from, sample_small_int
import random
import tiktoken
from typing import Tuple, List, Optional
import math
from functools import reduce


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

class Boolean(Template):

    def generate(self, *args) -> List[Tuple[str, dict]]:
        x = self.gen_tree()
        return [(self.traverse(x), {})]

    # Give next move probabilities proportional to the inverse square root of the length of the move
    # (shifted so the min length move has probability weight 1)
    def smart_select(self, moves):
        strs = [self.get_str(x) for x in moves]
        lens = [len(x) for x in strs]
        probs = [x - min(lens) + 1 for x in lens]
        probs = [1./x**.5 for x in probs]
        return random.choices(moves, probs)[0]

    def traverse(self, orig, max_moves=5):

        txt = "Original: " + self.get_str(orig)
        prev_configs = [orig]
        moves = [x for x in self.get_moves(orig) if self.get_str(x) not in [self.get_str(y) for y in prev_configs]]
        # Can't go back
        moves = remove_duplicates(moves, self.get_str)
        count = 0
        while len(moves) > 0 and count < max_moves:
            txt += "\n\nOptions:\n"
            txt += "\n".join([self.get_str(x) for x in moves])
            chosen_move = self.smart_select(moves)
            txt += "\nChosen: " + self.get_str(chosen_move)
            prev_configs.append(chosen_move)
            moves = [x for x in self.get_moves(chosen_move) if self.get_str(x) not in [self.get_str(y) for y in prev_configs]]
            moves = remove_duplicates(moves, self.get_str)
            count += 1
        
        return txt


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
                    if isinstance(x.operands[0], self.Leaf):
                        return "¬" + rec(x.operands[0])
                    return "¬(" + rec(x.operands[0]) + ")"
                elif x.operation == "AND":
                    op1_str = self.get_str(x.operands[0]) if isinstance(x.operands[0], self.Leaf) else "(" + self.get_str(x.operands[0]) + ")"
                    op2_str = self.get_str(x.operands[1]) if isinstance(x.operands[1], self.Leaf) else "(" + self.get_str(x.operands[1]) + ")"
                    return op1_str + " ∧ " + op2_str
                elif x.operation == "OR":
                    op1_str = self.get_str(x.operands[0]) if isinstance(x.operands[0], self.Leaf) else "(" + self.get_str(x.operands[0]) + ")"
                    op2_str = self.get_str(x.operands[1]) if isinstance(x.operands[1], self.Leaf) else "(" + self.get_str(x.operands[1]) + ")"
                    return op1_str + " ∨ " + op2_str
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
                    # 4a
                    if isinstance(op1, self.Op) and op1.operation == "NOT":
                        if self.get_str(op1.operands[0]) == self.get_str(op2):
                            new_forms.append(self.Leaf("0"))
                    if isinstance(op2, self.Op) and op2.operation == "NOT":
                        if self.get_str(op2.operands[0]) == self.get_str(op1):
                            new_forms.append(self.Leaf("0"))
                    # 6a (commutativity)
                    new_forms.append(self.Op(expr.operation, [op2, op1]))
                    # 7a (associativity)
                    if isinstance(op2, self.Op) and op2.operation == "AND":
                        new_forms.append(self.Op(expr.operation, [self.Op(expr.operation, [op1, op2.operands[0]]), op2.operands[1]]))
                    if isinstance(op1, self.Op) and op1.operation == "AND":
                        new_forms.append(self.Op(expr.operation, [op1.operands[0], self.Op(expr.operation, [op1.operands[1], op2])]))
                    # 8a (distributive)
                    if isinstance(op2, self.Op) and op2.operation == "OR":
                        new_forms.append(self.Op("OR", [self.Op("AND", [op1, op2.operands[0]]), self.Op("AND", [op1, op2.operands[1]])]))
                    return new_forms + \
                            [self.Op(expr.operation, [expr.operands[0], x]) for x in rec(expr.operands[1])] + \
                            [self.Op(expr.operation, [x, expr.operands[1]]) for x in rec(expr.operands[0])]
                elif expr.operation == "OR":
                    op1 = expr.operands[0]
                    op2 = expr.operands[1]
                    # 1b
                    if not isinstance(op1, self.Op) and op1.value == "1":
                        new_forms.append(self.Leaf("1"))
                    if not isinstance(op2, self.Op) and op2.value == "1":
                        new_forms.append(self.Leaf("1"))
                    # 2b
                    if not isinstance(op1, self.Op) and op1.value == "0":
                        new_forms.append(op2)
                    if not isinstance(op2, self.Op) and op2.value == "0":
                        new_forms.append(op1)
                    # 3b
                    if not isinstance(op1, self.Op) and not isinstance(op2, self.Op):
                        if op1.value == op2.value:
                            new_forms.append(op1)
                    # 4b
                    if isinstance(op1, self.Op) and op1.operation == "NOT":
                        if self.get_str(op1.operands[0]) == self.get_str(op2):
                            new_forms.append(self.Leaf("1"))
                    if isinstance(op2, self.Op) and op2.operation == "NOT":
                        if self.get_str(op2.operands[0]) == self.get_str(op1):
                            new_forms.append(self.Leaf("1"))
                    # 6b (commutativity)
                    new_forms.append(self.Op(expr.operation, [op2, op1]))
                    # 7b (associativity)
                    if isinstance(op2, self.Op) and op2.operation == "OR":
                        new_forms.append(self.Op(expr.operation, [self.Op(expr.operation, [op1, op2.operands[0]]), op2.operands[1]]))
                    if isinstance(op1, self.Op) and op1.operation == "OR":
                        new_forms.append(self.Op(expr.operation, [op1.operands[0], self.Op(expr.operation, [op1.operands[1], op2])]))
                    # 8b (distributive)
                    if isinstance(op2, self.Op) and op2.operation == "AND":
                        new_forms.append(self.Op("AND", [self.Op("OR", [op1, op2.operands[0]]), self.Op("OR", [op1, op2.operands[1]])]))
                    
                    return new_forms + \
                            [self.Op(expr.operation, [op1, x]) for x in rec(op2)] + \
                            [self.Op(expr.operation, [x, op2]) for x in rec(op1)]
                elif expr.operation == "NOT":
                    op1 = expr.operands[0]
                    if isinstance(op1, self.Leaf) and op1.value == "1":
                        new_forms.append(self.Leaf("0"))
                    if isinstance(op1, self.Leaf) and op1.value == "0":
                        new_forms.append(self.Leaf("1"))
                    # 5
                    if isinstance(op1, self.Op) and op1.operation == "NOT":
                        new_forms.append(op1.operands[0])
                    # 9a (DeMorgan's)
                    if isinstance(op1, self.Op) and op1.operation == "AND":
                        new_forms.append(self.Op("OR", \
                                [self.Op("NOT", [op1.operands[0]]), self.Op("NOT", [op1.operands[1]])]))
                    # 9b (DeMorgan's)
                    if isinstance(op1, self.Op) and op1.operation == "OR":
                        new_forms.append(self.Op("AND", \
                                [self.Op("NOT", [op1.operands[0]]), self.Op("NOT", [op1.operands[1]])]))
                    return new_forms + [self.Op(expr.operation, [x]) for x in rec(op1)]
                else:
                    raise NotImplementedError(f"Operation {x.operation} unrecognized")
            else:
                return new_forms
        moves = rec(x)
        
        moves = remove_duplicates(moves, self.get_str)
        return moves
    
    def gen_tree(self, max_depth=4, max_letters=2):
        letters = random.sample("ABCDEFGHIJKLMNOPQRSTUVWXYZ", max_letters)
        var_choices = letters + ["1", "0"]
        def rec(depth=1):
            if depth >= max_depth:
                return self.Leaf(random.choice(var_choices))
            choice = random.choice(['AND', 'OR', 'NOT'])
            if choice == "AND":
                new_op = self.Op("AND", [rec(depth+1), rec(depth+1)])
            elif choice == "OR":
                new_op = self.Op("OR", [rec(depth+1), rec(depth+1)])
            elif choice == "NOT":
                new_op = self.Op("NOT", [rec(depth+1)])
            else:
                raise NotImplementedError(f"Operation {choice} unrecognized")
            return new_op
        return rec()
