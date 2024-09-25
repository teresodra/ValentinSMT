import numpy as np

# distribution = np.random.uniform
# distribution_parameters = {'low': 10, 'high': 1500, 'size': 3}

distribution = np.random.chisquare
distribution_parameters = {'df': 10, 'size': 60}  # 'df' is degrees of freedom
times = 10


def generate_random_vector():
    # Generate 'size' random numbers uniformly distributed between 'low' and 'high'
    return distribution(**distribution_parameters) * times
