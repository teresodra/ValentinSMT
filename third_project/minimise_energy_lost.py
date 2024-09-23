import gurobipy as gp
from gurobipy import GRB
import math

def find_c_values_fixed_length_gurobi(p, max_c_acumulado=None):
    # if valid_range is None:
    #     aveg_p = sum(p) / len(p)
    #     valid_range = [aveg_p * math.sqrt(9 / 15), aveg_p * math.sqrt(15 / 9)]
    # print("P: ", p)
    # print("VALID RANGE: ", valid_range)
    if max_c_acumulado is None:
        max_c_acumulado = 70  # Maximum cumulative compensated value

    n = len(p)  # Number of elements in p

    # Create a new Gurobi model
    model = gp.Model("find_c_values")

    
    # Create continuous variables for c that can take negative values
    c = model.addVars(n, lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="c")
    slack = model.addVars(n, vtype=GRB.CONTINUOUS, name="slack")

    # Create continuous variables for valid_range
    valid_range = model.addVars(2, lb=0, vtype=GRB.CONTINUOUS, name="valid_range")
    ratio = model.addVar(lb=0, vtype=GRB.CONTINUOUS, name="ratio")

    # Add constraints
    for j in range(1, n + 1):
        model.addConstr(gp.quicksum(c[i] for i in range(j)) <= max_c_acumulado, name=f"cumulative_sum_{j}")
        # Here checking that there is not too much power in the compensating line
        # I also should check for negative, no?
        model.addConstr(gp.quicksum(c[i] for i in range(j)) >= -max_c_acumulado, name=f"cumulative_sum_{j}")

    for i in range(n):
        model.addConstr(p[i] - c[i] >= valid_range[0], name=f"range_min_{i}")
        model.addConstr(p[i] - c[i] <= valid_range[1] + slack[i], name=f"range_max_{i}")

    # Add constraint that the sum of the vector c must be 0
    model.addConstr(gp.quicksum(c[i] for i in range(n)) == 0, name="sum_c_zero")

    # Add constraints to enforce valid_range[1] / valid_range[0] <= 15 / 9
    model.addConstr(valid_range[1] <= ratio * valid_range[0], name="valid_range_ratio_constraint")
    model.addConstr(ratio == 15 / 9, name="ratio_upper_bound")


    # Set the objective to minimize the sum of slack variables
    model.setObjective(gp.quicksum(slack[i] for i in range(n)), GRB.MINIMIZE)

    # Optimize the model
    model.optimize()

    if model.status == GRB.OPTIMAL:
        c_values = [c[i].X for i in range(n)]
        min_slack_sum = model.objVal
        return True, c_values, min_slack_sum
    else:
        return False, None, None

# # Example usage:
# p = [10, 20, 30, 40, 1100]
# result, c_values, min_slack_sum = find_c_values_fixed_length_gurobi(p)
# print("Result:", result)
# if result:
#     print("C values:", c_values)
#     print("Minimum sum of slack variables:", min_slack_sum)
