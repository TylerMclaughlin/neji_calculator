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
    
def decimal(number):
    """
    Rounds string version of int to 6 decimal places for printing.
    """
    return "{:.6f}".format(number)

def pad(string, max_len):
    """
    add some leading spaces to string to bring it up to max_len.
    """
    string = str(string)
    return " "*(max_len - len(string)) + string

def get_neji(edo_list, generators, print_all_approx = False, nudge_degree = None, nudge_by = 0, limit_generators = False): 
    """
    argument edo_list is a collection of notes (cents).
    generators is a list of numbers, usually primes.
    """
    if limit_generators:
        denoms = generators
    else:    
        denoms = sorted(expand_generators(generators))
    # I'm intentionally not using Pandas for this one;
    # trying to keep the dependency list small.
    # I'd love to use data tables instead of lists for this,
    # it would make things nicer to read,
    # but i don't want the Pandas installation to prevent people from using my code! 
    edo_degree = []
    best_fractions = []
    best_matches = []
    best_errors = []
    for i, target_cents in enumerate(edo_list):
        best_num_for_denom = {}  # denom : best_numerator.
        for denom in denoms:
            num = round(find_numerator(target_cents, denom))
            neji_cents = cents_from_interval(num, denom)
            error = neji_cents - target_cents 
            edo_degree.append(i)
            best_matches.append(neji_cents)
            best_errors.append(error)
            best_fractions.append(Fraction(num, denom))

    # get max len for different substrings of the print out
    max_len_degree = len(str(len(edo_list) - 1))
    max_len_frac = len(str(denoms[-1]*2)) + 1 + len(str(denoms[-1])) # use the biggest generator to get the maximum size of the fraction
    max_len_cents = 4 + 1 + 6 # 4 spaces for 1200, 1 for the decimal point, and 6 for the trailing decimal places.

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

    final_cents = []
    for i, best_ix in enumerate(best_degree_approx_indices):
        neji_degree = edo_degree[best_ix]
        if nudge_degree is None or nudge_degree != i:
            # STANDARD PRINTING AND APPENDING, NO NUDGING
            final_cents.append(best_matches[best_ix])
            print(pad(neji_degree, max_len_degree), pad(best_fractions[best_ix],max_len_frac), pad(decimal(best_matches[best_ix]), max_len_cents), pad(decimal(best_errors[best_ix]),max_len_cents))
        # ATTEMPT TO NUDGE
        else:  # else nudge degree matches this edo degree.
            # because denoms is sorted, we can use denom as the largest denominator which is the largest generator product.
            nudged_fraction = best_fractions[best_ix] + Fraction(nudge_by, denom) 
            # make sure the nudged note doesn't overshoot or undershoot a neighboring note.
            if (nudge_by >= 0) and (nudged_fraction >= best_fractions[best_degree_approx_indices[i +1]]):
                raise ValueError(f'The amount you nudged degree {nudge_degree} will make it equal to or exceed neighboring degree {nudge_degree + 1}.  ' + \
                        'Please decrease the nudge by argument via "-b" or "--by".')
            elif (nudge_by < 0) and (nudged_fraction <= best_fractions[best_degree_approx_indices[i -1]]):
                raise ValueError(f'The amount you nudged degree {nudge_degree}  will make it less than or equal to neighboring degree {nudge_degree - 1}.  ' + \
                        'Please increase the nudge by argument via "-b" or "--by".')
            else: # COMMITING NUDGED INTERVAL TO DATA   
                nudged_cents = cents_from_interval(nudged_fraction.numerator, nudged_fraction.denominator)
                final_cents.append(nudged_cents)
                nudged_error = nudged_cents - edo_list[neji_degree]
                print(pad(neji_degree, max_len_degree), pad(nudged_fraction, max_len_frac), pad(decimal(nudged_cents), max_len_cents), pad(decimal(nudged_error), max_len_cents),\
                        f'(raised by {Fraction(nudge_by, denom)})' )
    return final_cents

def write_scala(name, cents_list):
    """ 
    name is a name for the file.  It currently must have underscores instead of spaces. 
    cents_list is a list of cents that starts at 0 and ends at 1200.  There is no 0 in the .scl file. 
    """
    filename = name + '.scl'
    file_string = f'! {filename}\n! Created using r tyler\'s neji calculator\n!\n{name}\n'
    file_string += f' {len(cents_list) - 1}\n!\n' # space here is intentional.
    cents_rows =  '\n '.join([str(cent) for cent in cents_list[1:]]) # scl format doesn't have the 0.
    file_string += f' {cents_rows}'
    with open(filename,'w') as f:
       f.write(file_string)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("n_edo", help="Number of divisions per octave.", type = int)
    parser.add_argument("generator_string", help="Comma-separated list of generators:  integers whose combinations of products are eligible for denominator.", type = str)
    parser.add_argument("name", help="Name for the output .scl file.  Use underscores instead of spaces.", type = str)
    parser.add_argument("-n","--nudge", help="Tuning degree to nudge. Counting starts at zero.", type = int)
    parser.add_argument("-b","--by", help="Amount to nudge by. Increments of 1 divided by the largest generator product. May be negative", default = 0, type = int)
    parser.add_argument("-l","--limit", help="Limit denominators to those listed -- that is, don't take the product.  Off by default.", const = True, default = False, action = 'store_const')
    args = parser.parse_args()
    if args.nudge is not None: 
        if args.nudge > args.n_edo:
            raise ValueError("The degree that gets nudged must be less than the specified N-EDO.")
        elif args.nudge == 0:
            print(f'Warning, you are nudging degree 0 of the scale. This is not supported right now! ')
    n_edo = args.n_edo 
    generators = [int(g) for g in args.generator_string.split(',')] 
    name = args.name 
    print(f'N-EDO: {n_edo}, Generators: {generators}, Filename: {name}.scl')
    print('')
    print('degree, ratio, cents, error (cents from EDO)')
    neji_cents_list = get_neji(cents_from_edo(int(n_edo)), generators, nudge_degree = args.nudge, nudge_by = args.by, limit_generators = args.limit)
    write_scala(name = name, cents_list = neji_cents_list)
