AVOGADRO = 6.02214076*(10**23)

def conc_in_um_to_no(conc_in_um, vol_in_l):
    return round(conc_in_um * 10**(-6) * vol_in_l * AVOGADRO)

def no_to_conc_in_um(no, vol_in_l):
    return no / (10**(-6) * vol_in_l * AVOGADRO)
