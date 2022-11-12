"""Método Montecarlo para aproximar la perdida esperada."""
from random import gammavariate
from min_lost import minimizar_perdida_de_potencia

reps = 1000  # veces que vamos a repetir el cálculo
n = 3  # numero de generadores
alpha = 2 # parametros para la funcion gammavariate
beta = 2

# Asumo que lo único que cambia son las potencias generadas, al resto
# le asignamos el valor deseado
min_voltaje = 300
max_voltaje = 600
voltaje_total = (min_voltaje+max_voltaje)/2*n
limites_en_voltaje = [[min_voltaje,max_voltaje]]*n

# Procedemos al cálculo de la perdida en reps scenarios
perdida_acumulada = 0
for i in range(reps):
    print(i)
    potencias_generadas = [gammavariate(alpha, beta) for _ in range(n)]
    perdida, _ = minimizar_perdida_de_potencia(voltaje_total, limites_en_voltaje, potencias_generadas)
    perdida_acumulada += perdida

print(perdida_acumulada/reps)