from z3 import *
import math


def find_c_values_fixed_length(p, valid_range=None, max_c_acumulado=None):
    if valid_range is None:
        aveg_p = sum(p)/len(p)
        valid_range = [aveg_p*math.sqrt(9/15), aveg_p*math.sqrt(15/9)] # Rango de 
    if max_c_acumulado is None:
        max_c_acumulado = 70  # Maximo compensado acumulado
    n = len(p)  # Number of elements in p
    solver = Solver()  # Initialize the Z3 solver
    
    # Create a list of integer variables for c
    c = [Int(f'c_{i}') for i in range(n)]
    
    # Cumulative sum constraint
    for j in range(1, n + 1):
        solver.add(Sum(c[:j]) < max_c_acumulado)  # sum of c from c_1 to c_j must be less than 70
    
    # Range constraints for each c_i relative to p_i
    for i in range(n):
        solver.add(p[i] - c[i] > valid_range[0])  # p_i - c_i must be greater than
        solver.add(p[i] - c[i] < valid_range[1]) # p_i - c_i must be less than

    # Check if a solution exists
    if solver.check() == sat:
        # model = solver.model()  # Get the model if it exists
        # c_values = [model.eval(c[i]).as_long() for i in range(n)]  # Extract the solution
        return True#, c_values
    else:
        return False#, None
    

# def find_c_values(p):
#     aveg_p = sum(p)/len(p)
#     valid_range = [aveg_p*math.sqrt(9/15), aveg_p*math.sqrt(15/9)]
#     print(valid_range)
#     print(p)
#     i = 0
#     n = len(p)
#     while i < n:
#         j = n
#         condition = find_c_values_fixed_length(p[i:j], valid_range)
#         while not condition:
#             j -= 1
#             if i == j:
#                 return False
#         i = j
#     return True


# a = [2,41,3]
# print(a[0:0])

# p = [440/5.6, ]


# # Example usage
# # p = [120, 150, 180, 130]  # Example p values
# p = [100*math.sqrt(9/15)+11,100*math.sqrt(9/15)-10,100*math.sqrt(15/9)-11,100*math.sqrt(15/9)+10]
# possible = find_c_values(p)
# if possible:
#     print("It is possible to find such c values:")
# else:
#     print("No valid c values can be found.")
