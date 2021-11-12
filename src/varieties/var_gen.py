#!/usr/bin/env python3
"""
This script generates all varieties up to certain index n, which is 10 by default.
This is based on https://arxiv.org/pdf/1911.05817.pdf.
"""

import sys

def recur_gen_varieties(n):
    if n == 2:
        G = [[2, 1]]
        H = [[2]]
        I = [[2, 1, 2]]
    else:
        G, H, I = recur_gen_varieties(n - 1)

        Gn = [n] + G[-1][::-1]
        G.append(Gn)
        
        Hn = Gn + [n] + H[-1][::-1]
        H.append(Hn)
        
        In = Gn + [n] + I[-1][::-1]
        I.append(In)

    return [G, H, I]


def gen_varieties(n):
    """ Generates all varieties, G, H, I, up to order n, n >= 2.
        G2 = x2x1, H2 = x2, I2 = x2x1x2,
        and Gn = xn|Gn−1|, Hn = Gnxn|Hn−1|, In = Gnxn|In−1|, for all n ≥ 3,
        where |Gn-1| means Gn-1 with the elements in the list reversed.
    Args:
        n (int): max order to generate
    Returns:
        (List[list[List]]): List of G, H, I, each of which are lists up to order n.
    """
    if n < 2:
        return [[], [], []]

    return recur_gen_varieties(n)


def make_variety_str(V):
    """ Construct strings that Mace4 understands: e.g. ((X3 * x1) * x2) from [2, 1, 2]
    Args:
        V (list(list[int])): list of list of subscripts for varieties. Each component list
                             is a G/H/I variety for a specific order.
    Returns:
        (list[Str]): list of strings, one for each order, for the variety of that order
    """
    Vstr = []
    for variety in V:
        clause = f"x{variety[0]}"
        for y in range(1, len(variety)):
            clause = f"({clause} * x{variety[y]})"
        Vstr.append(clause)
    return Vstr


def debug_print(v):
    for index, item in enumerate(['G', 'H', 'I']):
        print(f"{item}:")
        print(v[index])


def make_varieties(n):
    """ Construct the varieties up to index n
    Args:
        n (int): index
    Returns:
        (List[List[Str]]): list of list of variety strings for each level, starting at index 2
    """
    G, H, I = gen_varieties(n)
    Gstr = make_variety_str(G)
    Hstr = make_variety_str(H)
    Istr = make_variety_str(I)
    return [Gstr, Hstr, Istr]


if __name__ == "__main__":
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    else:
        n = 10
    v = make_varieties(n)
    debug_print(v)
    
    
__all__ = ['gen_varieties']
    