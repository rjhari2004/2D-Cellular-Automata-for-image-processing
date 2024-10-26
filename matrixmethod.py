import numpy as np
import pandas as pd
# Function to create T1 and T2 matrices dynamically based on image size
def create_matrices(image_shape):
    n = image_shape[0]
    T1 = np.zeros((n, n), dtype=int)
    T2 = np.zeros((n, n), dtype=int)

    # Fill T1 and T2 based on the general pattern
    for i in range(n - 1):
        T1[i, i + 1] = 1
    T2[1:n, 0:n-1] = np.eye(n - 1, dtype=int)

    return T1, T2

# Decompose rule number into powers of 2
def decompose_rule_number(rule_num):
    powers = []
    power = 1
    while rule_num > 0:
        if rule_num & 1:
            powers.append(power)
        rule_num >>= 1
        power <<= 1
    return powers

# Apply transformations based on decomposed rule
def apply_rule(rule_num, image):
    T1, T2 = create_matrices(image.shape)  # Create T1, T2 based on image size
    rule_transform = {
        1: lambda x: x,
        2: lambda x: np.dot(x,T2) % 2,
        4: lambda x: np.dot(T1, np.dot(x,T2)) % 2,
        8: lambda x: np.dot(T1, x) % 2,
        16: lambda x: np.dot(T1, np.dot(x,T1)) % 2,
        32: lambda x: np.dot(x,T1) % 2,
        64: lambda x: np.dot(T2, np.dot(x,T1)) % 2,
        128: lambda x: np.dot(T2,x) % 2,
        256: lambda x: np.dot(T2, np.dot(x,T2)) % 2
    }

    powers = decompose_rule_number(rule_num)
    result_image = np.zeros_like(image)

    for power in powers:
        if power in rule_transform:
            transformed_image = rule_transform[power](image)
            result_image = (result_image + transformed_image) % 2  # XOR operation

    return result_image

# Function to iterate over steps and print results
def cellular_automata(rule_num, grid, steps=10):
    image = grid
    for step in range(steps+1):
        print(f"Step {step}:\n", image)
        DF = pd.DataFrame(image) 
        DF.replace(0, np.nan, inplace=True)
        DF.to_csv(f"Step_{step}_matrix.csv", index=False, header=False, na_rep='')
        image = apply_rule(rule_num, image)
        print("\n")

# Input functions
def input_image():
    rows = int(input("Enter the number of rows for the image: "))
    print("Enter each row as a space-separated list of 0s and 1s, each row on a new line:")
    image = []
    for _ in range(rows):
        row = list(map(int, input().strip().split()))
        image.append(row)
    return np.array(image)

def input_grid_size():
    return int(input("Enter the size of the grid (it will be a square grid): "))

def position_image_in_grid(grid_size, image):
    grid = np.zeros((grid_size, grid_size), dtype=int)
    # Calculate position to place the image in the center
    start_row = (grid_size - image.shape[0]) // 2
    start_col = (grid_size - image.shape[1]) // 2
    grid[start_row:start_row + image.shape[0], start_col:start_col + image.shape[1]] = image
    return grid

# Main execution
rule_number = int(input("Enter the rule number: "))
initial_image = input_image()
grid_size = input_grid_size()
steps = int(input("Enter the number of steps: "))

# Position the image in the center of the grid
initial_grid = position_image_in_grid(grid_size, initial_image)

# Run cellular automata
cellular_automata(rule_number, initial_grid, steps)
