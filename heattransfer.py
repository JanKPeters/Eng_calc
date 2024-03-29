def conductive_resistance (L, k, A):
    Rk = 0
    Rk = L/(k*A)
    return Rk


def convective_resistance (h, A):
    Rh = 0
    Rh = 1/(h*A)
    return Rh

def conduction (T1, T2, R):
    Qcond = 0
    Qcond = (T1-T2)/R
    return Qcond


def heat_transfer_coef (v):
    h = 0
    h = 10.45-v+10*v**0.5
    return h


def layer_temperature (Q, R, T1):
    Tl = 0
    Tl = T1 - Q * R
    return Tl
