"""
This Calculator can be used to compare efficiency between different heat
exchangers. The goal is to be able to measure excess CO2 from heat exchanger
exhaust; however, the exhaust has to be cool enough to measure CO2


Variables::
    Convection Coefficients -------- hp, ha
    Exchanger Coefficient ---------- U

"""
import math


def __hp(id, od):
    hi = 684
    return hi * id / od


def r_coeff(mc, cpc, mw, cpw):
    return (mc * cpc) / (mw * cpw)


def a_null(Dp, L):
    return math.pi * Dp * L


def u_null(id, od):
    hp = __hp(id, od)
    ha = 417
    return 1 / ((1/hp)+(1/ha))


def e_coeff(counter, R, Mc, Cpc):
    """
    print(round(e_coeff(False, 8.64, 3.66, 30000, 0.608), 3))
    """
    outer = 1.375 / 12
    inner = outer + .007
    U = u_null(inner, outer)
    A = a_null(outer, 24)
    if counter:
        return math.e ** ((U * A * (R - 1)) / (Mc * Cpc))
    else:
        return math.e ** ((U * A * (R + 1)) / (Mc * Cpc))


def counterflow(hot, T, t, R):
    """ This function computes the heat exchange for a counterflow design """
    e = e_coeff(True, 3.66, 30000, 0.608)
    T2 = round((T * (R - 1) - R * t * (1 - 1.375)) / (
              (R * e) - 1), 1)
    if hot:
        return T2
    else:
        return round(t + ((T - T2) / R), 1)


def parallel(hot, T, t, R):
    """ This function computes the heat exchange for a parallel design """
    e = e_coeff(False, 3.66, 30000, 0.608)
    T2 = round((((R + e) * T) + ((R * t) * (e - 1))) / ((R + 1)
               * e), 1)
    if hot:
        return T2
    else:
        return round(t + ((T - T2) / R), 1)


def main():
    R, Mc, Cpc = 3.66, 30000, 0.608

    print(e_coeff(True, R, Mc, Cpc))

    print(parallel(False, 175, 90, 3.66))
    print(parallel(True, 175, 90, 3.66))
    print(counterflow(False, 175, 90, 3.66))
    print(counterflow(True, 175, 90, 3.66))



if __name__ == '__main__':
    main()