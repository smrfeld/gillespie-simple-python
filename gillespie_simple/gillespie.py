from .counts import *
from .rxn import *
from .helpers import *

import scipy.special
import numpy as np
import copy


def get_prop(rate, species_multiplicity, counts):
    prop = rate
    for species, mult in species_multiplicity.items():
        count = counts.get_count(species)
        prop *= scipy.special.binom(count, mult)
    return prop


def choose_next_rxn(rxn_list, counts):

    props = []

    for rxn in rxn_list:
        if len(rxn.r_list) != 0:
            props.append(get_prop(rxn.kr, rxn.species_r_multiplicity, counts))
        else:
            props.append(get_prop(rxn.kr, rxn.species_p_multiplicity, counts))

    props_cum = sum(props)

    # No rxns left?
    if props_cum <= 1.0e-8:
        return [None, None]

    # Choose the reaction
    try:
        rxn_chosen = np.random.choice(rxn_list,size=1,p=np.array(props)/props_cum)[0]
    except:
        print("Something went wrong. Likely a propensity is negative?")
        print("Counts:")
        print(counts)
        print("")
        print("Propensities:")
        print(props)
        print("")
        print("Reactions:")
        for rxn in rxn_list:
            print(rxn)
            print("")

    # Time
    dt_next = np.log(1.0 / np.random.rand()) / props_cum

    return [rxn_chosen, dt_next]


def do_rxn(rxn, counts):

    for species, mult in rxn.species_r_multiplicity.items():
        counts.increment_count(species, -1 * mult)

    for species, mult in rxn.species_p_multiplicity.items():
        counts.increment_count(species, mult)


def run_gillespie(rxn_list, counts, dt_st_every, t_max, verbose=True, conserved_species=[], write_as_we_go=False, write_dir=None):

    # Check args
    if write_as_we_go and write_dir == None:
        raise ValueError("Must specify write_dir if we are to write as we go.")

    # Setup writing if needed
    if write_as_we_go:
        if write_dir[-1] != "/":
            write_dir += "/"

        for species in counts.get_species():
            f = open(write_dir + species + ".txt", "w")
            f.close()

    # Store init counts to conserve species
    counts_init = copy.deepcopy(counts)

    # Setup count storage
    counts_hist = CountsHist()
    counts_hist.store_counts(0, counts)
    t_st_next = dt_st_every

    # Run
    t_curr = 0
    while t_curr < t_max:

        # Pick rxn
        rxn_next, dt_next = choose_next_rxn(rxn_list, counts)

        # Check if any left
        if rxn_next == None:
            break

        # Store
        while t_st_next < t_curr + dt_next:

            if verbose:
                print("%.2f / %.2f" % (t_st_next, t_max))

            # Store
            counts_hist.store_counts(t_st_next, counts)

            # Write?
            if write_as_we_go:
                if write_dir[-1] != "/":
                    write_dir += "/"

                for species in counts.get_species():
                    f = open(write_dir + species + ".txt", "a")
                    f.write("%f %d\n" % (t_st_next, counts.get_count(species)))
                    f.close()

            # Advance storage time
            t_st_next += dt_st_every

        # Advance time
        t_curr += dt_next

        # Do the reaction
        do_rxn(rxn_next, counts)

        # Conserve species
        for species in conserved_species:
            counts.set_count(species, counts_init.get_count(species))

    return counts_hist
