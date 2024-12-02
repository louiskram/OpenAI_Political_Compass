"""
Takes in a list of politicalcompass links and averages the output per model
Outputs the respective links and creates a pyplot
Made with ChatGPT
"""

import os
import re
from collections import defaultdict
import matplotlib.pyplot as plt

# Path to the file containing the links
file_path = "outputs/2024-12-02-08-40-22/links.txt"

# Dictionary to store the extracted values for each model
data = defaultdict(list)

# Regular expression to extract model names and values from the links
pattern = re.compile(r'^(.*?):.*?ec=(-?\d+\.\d+)&soc=(-?\d+\.\d+)$')

# Read and process the file
with open(file_path, "r") as file:
    for line in file:
        line = line.strip()
        match = pattern.match(line)
        if match:
            model = match.group(1).rsplit("-", 1)[0]  # Extract the model name (without index)
            ec = float(match.group(2))  # Economic value
            soc = float(match.group(3))  # Social value
            data[model].append((ec, soc))

# Calculate the average values for each model
averages = {}
for model, values in data.items():
    avg_ec = sum(ec for ec, soc in values) / len(values)
    avg_soc = sum(soc for ec, soc in values) / len(values)
    averages[model] = (avg_ec, avg_soc)

base_url = "https://www.politicalcompass.org/analysis2"

# Output the results
print("Average values per model:")
for model, (avg_ec, avg_soc) in averages.items():
    # print(f"{model}: Economic = {avg_ec:.2f}, Social = {avg_soc:.2f}")
    link = f"{base_url}?ec={avg_ec:.2f}&soc={avg_soc:.2f}"
    print(f"{model}: Economic = {avg_ec:.2f}, Social = {avg_soc:.2f}, Url = {link}")

# Extract model names, economic (x), and social (y) values
models = list(averages.keys())
x_values = [coord[0] for coord in averages.values()]  # Economic axis
y_values = [coord[1] for coord in averages.values()]  # Social axis

# Plot the Political Compass
plt.figure(figsize=(8, 8))
plt.axhline(0, color='black', linewidth=0.8)  # Horizontal axis
plt.axvline(0, color='black', linewidth=0.8)  # Vertical axis

# Plot the points with labels
for model, x, y in zip(models, x_values, y_values):
    plt.scatter(x, y, label=model)
    plt.text(x + 0.1, y, model, fontsize=9)

# Set plot limits and labels
plt.xlim(-10, 10)
plt.ylim(-10, 10)
plt.title("Political Compass Plot")
plt.xlabel("Economic Left/Right")
plt.ylabel("Social Libertarian/Authoritarian")

# Add grid and legend
plt.grid(color='gray', linestyle='--', linewidth=0.5)
plt.legend(loc='upper left', fontsize=8)

output_folder = "outputs/2024-12-02-08-40-22"
output_file = os.path.join(output_folder, "political_compass_plot.png")
plt.savefig(output_file, dpi=300, bbox_inches='tight')

# Show the plot
plt.show()