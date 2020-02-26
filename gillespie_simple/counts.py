import numpy as np
import glob
import os

class Counts:

    def __init__(self):
        self._counts = {}

    def set_count(self, species, count):
        if not species in self._counts:
            self._counts[species] = count
        else:
            self._counts[species] = count

        assert self._counts[species] >= 0

    def increment_count(self, species, increment):
        if not species in self._counts:
            self._counts[species] = increment
        else:
            self._counts[species] += increment

        assert self._counts[species] >= 0

    def get_count(self, species):
        if species in self._counts:
            return self._counts[species]
        else:
            return 0

    def get_species(self):
        return list(self._counts.keys())

    def __str__(self):
        s = ""
        for species, count in self._counts.items():
            s += "%s: %d\n" % (species, count)

        return s


class CountsHist:

    def __init__(self):
        self._counts_hist = {}
        self._t_hist = []

    def store_counts(self, time, counts):
        self._t_hist.append(time)

        for species in counts.get_species():
            count = counts.get_count(species)

            if not species in self._counts_hist:
                self._counts_hist[species] = (len(self._t_hist) - 1) * [0]

            self._counts_hist[species].append(count)

            assert len(self._counts_hist[species]) == len(self._t_hist)

    def get_count_hist(self, species):
        return [self._t_hist, self._counts_hist[species]]

    def write_count_hist(self, species, fname):
        f = open(fname, 'w')
        for idx, time in enumerate(self._t_hist):
            f.write("%f %f\n" % (time, self._counts_hist[species][idx]))
        f.close()

    def write_all_count_hists(self, dir_name):
        if dir_name[-1] != "/":
            dir_name += "/"

        for species, counts in self._counts_hist.items():
            f = open(dir_name + species + ".txt", "w")
            for idx, time in enumerate(self._t_hist):
                f.write("%f %d\n" % (time, counts[idx]))
            f.close()

    def read_all_count_hists(self, dir_name):
        if dir_name[-1] != "/":
            dir_name += "/"

        files = glob.glob(dir_name+"*.txt")
        bases = [os.path.basename(x) for x in files]
        species_list = [os.path.splitext(base)[0] for base in bases]

        # Clear
        self._counts_hist = {}
        self._t_hist = []
        for idx, file in enumerate(files):
            species = species_list[idx]

            self._counts_hist[species] = []

            f = open(file, "r")
            for line in f:
                s = line.split()
                if len(s) == 2:
                    time = float(s[0])
                    count = int(s[1])

                    # Only store time list for one of the files
                    if idx == 0:
                        self._t_hist.append(time)

                    self._counts_hist[species].append(count)

            f.close()

        # Check that all have the same length
        for species, counts in self._counts_hist.items():
            assert len(self._t_hist) == len(counts)


    def get_average_counts(self, time_start):
        idx_start = next(x[0] for x in enumerate(self._t_hist) if x[1] >= time_start)

        counts_average = {}
        for species, counts in self._counts_hist.items():
            counts_average[species] = np.mean(counts[idx_start:])

        return counts_average

    def get_t_max(self):
        return self._t_hist[-1]
