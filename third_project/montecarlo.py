from general import generate_random_vector
from possible_to_compensate import find_c_values_fixed_length
from minimise_energy_lost import find_c_values_fixed_length_gurobi
import matplotlib.pyplot as plt

M = 500
loss = []
all_p = 0
for i in range(M):
    print(i)
    p = generate_random_vector()
    # if find_c_values_fixed_length(p):
    result, c_values, min_slack_sum = find_c_values_fixed_length_gurobi(p)
    if result is False:
        raise Exception("How can this happen?")
    loss.append(min_slack_sum)
    all_p += sum(p)

print(f"The percentage of energy lost is: {round(sum(loss)/all_p*100, 2)}%")
print(sum(loss)/M)

# Creating a histogram
plt.hist(loss, bins=20, edgecolor='black')

# Adding title and labels
plt.title('Histogram of p values')
plt.xlabel('Value')
plt.ylabel('Frequency')

# Displaying the histogram
plt.show()
