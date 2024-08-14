import numpy as np
import scipy.stats as stats
import math

# Function to perform a Z-test
def z_test(sample_mean, population_mean, population_std, sample_size, alpha, calc_ci=False):
    z = (sample_mean - population_mean) / (population_std / math.sqrt(sample_size))
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))

    print(f"Z-test statistic: {z}")
    print(f"P-value: {p_value}")

    if calc_ci:
        margin_of_error = stats.norm.ppf(1 - alpha/2) * (population_std / math.sqrt(sample_size))
        ci_lower = sample_mean - margin_of_error
        ci_upper = sample_mean + margin_of_error
        print(f"{100 * (1 - alpha)}% Confidence Interval: ({ci_lower}, {ci_upper})")

    if p_value < alpha:
        print("Reject the null hypothesis")
    else:
        print("Fail to reject the null hypothesis")

# Function to perform a T-test
def t_test(sample_mean, population_mean, sample_std, sample_size, alpha, calc_ci=False):
    t = (sample_mean - population_mean) / (sample_std / math.sqrt(sample_size))
    df = sample_size - 1
    p_value = 2 * (1 - stats.t.cdf(abs(t), df))

    print(f"T-test statistic: {t}")
    print(f"P-value: {p_value}")

    if calc_ci:
        margin_of_error = stats.t.ppf(1 - alpha/2, df) * (sample_std / math.sqrt(sample_size))
        ci_lower = sample_mean - margin_of_error
        ci_upper = sample_mean + margin_of_error
        print(f"{100 * (1 - alpha)}% Confidence Interval: ({ci_lower}, {ci_upper})")

    if p_value < alpha:
        print("Reject the null hypothesis")
    else:
        print("Fail to reject the null hypothesis")

# Function to perform a paired T-test
def paired_t_test(sample1, sample2, alpha, calc_ci=False):
    differences = np.array(sample1) - np.array(sample2)
    mean_diff = np.mean(differences)
    std_diff = np.std(differences, ddof=1)
    sample_size = len(differences)
    t = mean_diff / (std_diff / math.sqrt(sample_size))
    df = sample_size - 1
    p_value = 2 * (1 - stats.t.cdf(abs(t), df))

    print(f"Paired T-test statistic: {t}")
    print(f"P-value: {p_value}")

    if calc_ci:
        margin_of_error = stats.t.ppf(1 - alpha/2, df) * (std_diff / math.sqrt(sample_size))
        ci_lower = mean_diff - margin_of_error
        ci_upper = mean_diff + margin_of_error
        print(f"{100 * (1 - alpha)}% Confidence Interval: ({ci_lower}, {ci_upper})")

    if p_value < alpha:
        print("Reject the null hypothesis")
    else:
        print("Fail to reject the null hypothesis")

# Main function to run the hypothesis testing tool
def main():
    print("Hypothesis Testing Tool")
    
    # User inputs
    test_type = input("Choose the test type (z/t/paired-t): ").strip().lower()
    alpha = float(input("Enter the significance level (alpha): "))
    calc_ci = input("Would you like to calculate the confidence interval? (yes/no): ").strip().lower() == 'yes'

    if test_type == 'z':
        sample_mean = float(input("Enter the sample mean: "))
        population_mean = float(input("Enter the population mean (null hypothesis): "))
        sample_size = int(input("Enter the sample size: "))
        population_std = float(input("Enter the population standard deviation: "))
        z_test(sample_mean, population_mean, population_std, sample_size, alpha, calc_ci)
    
    elif test_type == 't':
        sample_mean = float(input("Enter the sample mean: "))
        population_mean = float(input("Enter the population mean (null hypothesis): "))
        sample_size = int(input("Enter the sample size: "))
        sample_std = float(input("Enter the sample standard deviation: "))
        t_test(sample_mean, population_mean, sample_std, sample_size, alpha, calc_ci)
    
    elif test_type == 'paired-t':
        sample1 = list(map(float, input("Enter the first set of observations (comma-separated): ").split(',')))
        sample2 = list(map(float, input("Enter the second set of observations (comma-separated): ").split(',')))
        if len(sample1) != len(sample2):
            print("Error: The two samples must have the same number of observations.")
        else:
            paired_t_test(sample1, sample2, alpha, calc_ci)
    
    else:
        print("Invalid test type! Please choose either 'z', 't', or 'paired-t'.")

if __name__ == "__main__":
    main()
