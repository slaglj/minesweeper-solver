# Code copied from python docs (powerset recipe):
# https://docs.python.org/3/library/itertools.html
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    
    # added import
    from itertools import combinations, chain
    
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

    