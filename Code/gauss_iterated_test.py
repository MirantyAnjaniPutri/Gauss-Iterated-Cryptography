import math
import random
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chisquare

def chi_square_test(x, alpha, omega, K, beta, iterations):
    result = []
    for _ in range(iterations):
        x = math.exp(-alpha * (5/4 * ((x + omega + K / (2 * math.pi) * math.sin(2 * math.pi * x)) % 1) - 1/2)**2 + beta)
        y = int(x * 10**13 % 10)
        result.append(y)

    bin_counts, _ = np.histogram(result, bins=10, range=(0,10))

    expected_counts = np.full_like(bin_counts, fill_value=len(result)/len(bin_counts))
    expected_counts[expected_counts == 0] = 1  # Replace any zero with one
    
    chi_stat, p_value = chisquare(bin_counts, expected_counts)

     # Output the results
    print(f"Chi-Square Statistic: {chi_stat}, P-value: {p_value}")

    return p_value

def calculate_lyapunov_exponent(x, alpha, omega, K, beta, iterations):
    sum_log_deriv = 0
    for _ in range(iterations):
        # Calculate the derivative of the map at x
        derivative = abs(-alpha * (5/4) * 2 * (x + omega + K / (2 * math.pi) * math.sin(2 * math.pi * x)) * math.exp(-alpha * (5/4 * ((x + omega + K / (2 * math.pi) * math.sin(2 * math.pi * x)) % 1) - 1/2)**2))
        sum_log_deriv += math.log(derivative)
        
        # Update x using the Gauss iterated map
        x = math.exp(-alpha * (5/4 * ((x + omega + K / (2 * math.pi) * math.sin(2 * math.pi * x)) % 1) - 1/2)**2 + beta)
    
    # Calculate the Lyapunov exponent
    lyapunov_exponent = sum_log_deriv / iterations
    return lyapunov_exponent

def iterate_lyapunov_exponents(initial_values, alpha, omega, K, beta, iterations):
    results = {}
    for initial_x in initial_values:
        lyap_exp = calculate_lyapunov_exponent(initial_x, alpha, omega, K, beta, iterations)
        results[initial_x] = lyap_exp
    return results

def bifurcation_diagram(initial_x, alpha, omega, K, beta, alpha_start, alpha_end, alpha_step, iterations, last_n):
    """Generate a bifurcation diagram for the Gauss Iterated Map."""
    alpha_values = np.arange(alpha_start, alpha_end, alpha_step)
    bifurcation_data = []

    x = initial_x

    for alpha in alpha_values:
        temp_values = []

        # Iterate the map and store the last n values to plot
        for _ in range(iterations + last_n):
            x = math.exp(-alpha * (5/4 * ((x + omega + K / (2 * math.pi) * math.sin(2 * math.pi * x)) % 1) - 1/2)**2 + beta)
            if _ >= iterations:
                temp_values.append(x)

        bifurcation_data.extend([(alpha, value) for value in temp_values])

    # Plot the bifurcation diagram
    plt.figure(figsize=(10, 7))
    plt.plot(*zip(*bifurcation_data), ',')
    plt.title('Bifurcation Diagram')
    plt.xlabel('Alpha')
    plt.ylabel('X values')
    plt.show()

def main():
    # Define the parameters
    alpha = 9
    omega = 0.5
    K = 1000000
    beta = 0.481
    iterations = 10000

    initial_values = []
    lyapunov_exponents = []

    # Get the result of random initial value
    with open('lyapunov_exponents_test.txt', 'w') as file:
        for _ in range(1000):
            initial_x = random.random()  # Generates a random float number between 0 and 1
            lyapunov_exp = calculate_lyapunov_exponent(initial_x, alpha, omega, K, beta, iterations)
            # Create a txt file of the result
            file.write(f"Initial value: {initial_x}, Lyapunov Exponent: {lyapunov_exp}\n")

            # Append the results to the lists
            initial_values.append(initial_x)
            lyapunov_exponents.append(lyapunov_exp)

    # Plot the results
    plt.scatter(initial_values, lyapunov_exponents, s=1)  # s is the size of the points
    plt.xlabel('Initial Value')
    plt.ylabel('Lyapunov Exponent')
    plt.title('Lyapunov Exponents from Random Initial Values')
    plt.show()

    #Calculate Chi Square
    p_value = chi_square_test(random.random(), alpha, omega, K, beta, iterations)
    if p_value < 0.05:
        print("The distribution of states does not fit the expected uniform distribution.")
    else:
        print("The distribution of states fits the expected uniform distribution.")

    #Calculate the bifurcation diagram
    bifurcation_diagram(random.random(), alpha, omega, K, beta, 0, 10, 0.01, 1000, 100)
    

if __name__ == "__main__":
    main()