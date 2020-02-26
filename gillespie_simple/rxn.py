class Rxn:

    def __init__(self, name, kr, r_list, p_list):
        self.name = name
        self.kr = kr
        self.r_list = r_list
        self.p_list = p_list

        if len(r_list) == 0 and len(p_list) == 0:
            raise ValueError("Empty rxns are forbidden.")

        self.species = []
        for s in self.r_list:
            if not s in self.species:
                self.species.append(s)
        for s in self.p_list:
            if not s in self.species:
                self.species.append(s)

        self.species_r_multiplicity = {}
        for species in self.species:
            if species in self.r_list:
                self.species_r_multiplicity[species] = self.r_list.count(species)

        self.species_p_multiplicity = {}
        for species in self.species:
            if species in self.p_list:
                self.species_p_multiplicity[species] = self.p_list.count(species)

    def __str__(self):
        s = "%s\n" % self.name
        s += "kr: %.2f\n" % self.kr
        s += " ".join(self.r_list) + " -> " + " ".join(self.p_list)

        return s
