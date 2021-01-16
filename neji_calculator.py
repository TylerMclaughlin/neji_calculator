import argparse
import numpy as np
from itertools import chain, combinations
from fractions import Fraction

def cents_from_edo(n_edo):
    """
    A simple calculation to get a list of cents that corresponds to the pitches in an EDO.
    """
    cent_step = 1200/n_edo
    # this part will only work for n_edo as an integer.
    return [cent_step*i for i in range(0,n_edo + 1)]

def cents_from_interval(num, denom):
    return 1200*np.log2(num / denom)

def find_numerator(cents, denom):
    """
    This is the algebraic inverse of cents_from_interval().
    """
    return denom * 2 **(cents/1200)


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def expand_generators(generators):
    return [np.prod(x) for x in powerset(generators) if x != ()]
    

def get_neji(edo_list, generators, print_all_approx = False): 
    """
    argument edo_list is a collection of notes (cents).
    generators is a list of numbers, usually primes.
    """
    denoms = expand_generators(generators)
    # I'm intentionally not using Pandas for this one;
    # trying to keep the dependency list small.
    edo_degree = []
    best_fractions = []
    best_matches = []
    best_errors = []
    for i, target_cents in enumerate(edo_list):
        best_num_for_denom = {}  # denom : best_numerator.
        for d in denoms:
            num = round(find_numerator(target_cents, d))
            neji_cents = cents_from_interval(num, d)
            error = neji_cents - target_cents 
            edo_degree.append(i)
            best_matches.append(neji_cents)
            best_errors.append(error)
            best_fractions.append(Fraction(num, d))

    if print_all_approx: # print all approximations rather than just the best ones.
        for i, d in enumerate(edo_degree):
            print(i, d, best_fractions[i], best_matches[i], best_errors[i]) 

    # now find the best approximation for each edo scale degree from our generator/numerator combos.    
    unique_degrees = set(edo_degree)# alternatively speed up: list(range(i)) 
    best_degree_approx_indices = []
    for degree in unique_degrees: 
        #print(degree)
        degree_index_list = []
        for i, elem in enumerate(edo_degree):
            if len(degree_index_list) > len(denoms): # speeds up algorithm
                next
            if elem == degree:
               degree_index_list.append(i)
        min_error = 1200 # 1200 cents
        best_index = degree_index_list[0]
        for candidate_degree_approx_index in degree_index_list:
            candidate_error = best_errors[candidate_degree_approx_index]
            #print(candidate_degree_approx_index, candidate_error, min_error)
            if abs(candidate_error) < abs(min_error):
                min_error = candidate_error
                best_index = candidate_degree_approx_index
        best_degree_approx_indices.append(best_index)

    #print(best_degree_approx_indices)
    final_cents = []
    for ix in best_degree_approx_indices:
        final_cents.append(best_matches[ix])
        print(edo_degree[ix], best_fractions[ix], best_matches[ix], best_errors[ix])
    return final_cents

def write_scala(name, cents_list):
    """ 
    name is a name for the file.  It currently must have underscores instead of spaces. 
    cents_list is a list of cents that starts at 0 and ends at 1200.  There is no 0 in the .scl file. 
    """
    filename = name + '.scl'
    file_string = f'! {filename}\n! Created using R. Tyler\'s neji calculator\n!\n{name}\n'
    file_string += f' {len(cents_list) - 1}\n!\n' # space here is intentional.
    cents_rows =  '\n '.join([str(cent) for cent in cents_list[1:]]) # scl format doesn't have the 0.
    file_string += f' {cents_rows}'
    with open(filename,'w') as f:
       f.write(file_string)

if __name__ == '__main__':
    from sys import argv
    n_edo = argv[1] 
    generators = [int(g) for g in argv[2].split(',')] 
    name = argv[3] 
    print(n_edo, generators, name)
    neji_cents_list = get_neji(cents_from_edo(int(n_edo)), generators)
    write_scala(name = name, cents_list = neji_cents_list)
 
    
