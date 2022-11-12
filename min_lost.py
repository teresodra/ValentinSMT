from z3 import *


def minimizar_perdida_de_potencia(voltaje_total, limites_en_voltaje, potencias_generadas):
    n = len(potencias_generadas)
    I = Real('I')
    V = RealVector('V', n)


    s = Solver()
    for index, volt in enumerate(V):
        s.add(limites_en_voltaje[index][0] <= V[index], V[index] <= limites_en_voltaje[index][1])
        s.add(potencias_generadas[index] >= I*V[index])
    s.add(Sum(V) == voltaje_total)

    if s.check()==unsat:
        raise Exception("El voltaje total es demasiado alto o demasiado bajo")

    # el modelo se fija para que las constraints existentes no desaparezcan    
    s.push()

    highest_unsat = 0
    lowest_sat = 1

    potencia_perdida = lowest_sat
    s.add(sum([potencia_generada-V[index]*I for index, potencia_generada in enumerate(potencias_generadas)]) < potencia_perdida)

    # encontrando una potencia perdida posible
    while s.check() == unsat:
        s.pop()
        s.push()
        lowest_sat *= 2
        potencia_perdida = lowest_sat
        s.add(sum([potencia_generada-V[index]*I for index, potencia_generada in enumerate(potencias_generadas)]) < potencia_perdida)

    # tratando de encontrar la minima potencia perdida posible con un margen
    margen = 0.1
    while margen < lowest_sat - highest_unsat:
        print(lowest_sat, highest_unsat)
        potencia_perdida = (lowest_sat + highest_unsat)/2
        s.add(sum([potencia_generada-V[index]*I for index, potencia_generada in enumerate(potencias_generadas)]) < potencia_perdida)
        if s.check() == sat:
            lowest_sat = potencia_perdida
        else:
            s.pop()
            s.push()
            highest_unsat = potencia_perdida

    s.check()
    m = s.model()
    return potencia_perdida, m