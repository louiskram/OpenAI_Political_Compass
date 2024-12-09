"""
Takes in a list of politicalcompass links and averages the output per model per prompt
Outputs the respective links and creates a pyplot
Made with ChatGPT
"""
import argparse
import os
import re
from collections import defaultdict
import matplotlib.pyplot as plt

# Return the path of the newest directory within the specified parent directory
parent_directory = "outputs/"
subdirs = [os.path.join(parent_directory, d) for d in os.listdir(parent_directory) if os.path.isdir(os.path.join(parent_directory, d))]
newest_subdir = max(subdirs, key=os.path.getmtime)

# Read in input dir over command line
# Use newest directory in parent_directory if no argument is given
parser = argparse.ArgumentParser(description="Enter statements on Political Compass Test.")
parser.add_argument('--directory', type=str, default=newest_subdir, help='Input directory path')
args = parser.parse_args()
directory_path = args.directory or os.path.join(parent_directory, newest_subdir)

# Dictionary to store the extracted values for each model and prompt
data = defaultdict(lambda: defaultdict(list))

# Regular expression to extract model names, prompt indices, and values from the links
pattern = re.compile(r'^(.*?)-(?P<index>\d+)-prompt_(?P<prompt>\d+)\.json:.*?ec=(-?\d+\.\d+)&soc=(-?\d+\.\d+)$')

# Read and process the file
with open(os.path.join(directory_path, "links.txt"), "r") as file:
    for line in file:
        line = line.strip()
        match = pattern.match(line)
        if match:
            model = match.group(1)  # Extract the model name
            prompt_index = match.group("prompt")  # Extract the prompt index
            ec = float(match.group(4))  # Economic value
            soc = float(match.group(5))  # Social value
            data[model][prompt_index].append((ec, soc))

# Calculate the average values for each model and prompt
averages = defaultdict(dict)
for model, prompt_dict in data.items():
    for prompt_index, values in prompt_dict.items():
        avg_ec = sum(ec for ec, soc in values) / len(values)
        avg_soc = sum(soc for ec, soc in values) / len(values)
        averages[model][prompt_index] = (avg_ec, avg_soc)

base_url = "https://www.politicalcompass.org/analysis2"

# Output the results
print("Average values per model per prompt:")
for model, prompts in averages.items():
    for prompt_index, (avg_ec, avg_soc) in prompts.items():
        link = f"{base_url}?ec={avg_ec:.2f}&soc={avg_soc:.2f}"
        print(f"Model {model}, Prompt {prompt_index}: Economic = {avg_ec:.2f}, Social = {avg_soc:.2f}, Url = {link}")

# Prepare the data for plotting
models = []
x_values = []
y_values = []
labels = []

for model, prompts in averages.items():
    for prompt_index, (avg_ec, avg_soc) in prompts.items():
        models.append(model)
        x_values.append(avg_ec)
        y_values.append(avg_soc)
        labels.append(f"{model}-prompt_{prompt_index}")

# Plot the Political Compass
plt.figure(figsize=(8, 8))
plt.axhline(0, color='black', linewidth=0.8)  # Horizontal axis
plt.axvline(0, color='black', linewidth=0.8)  # Vertical axis

# Plot the points with labels for the legend, but without text annotations
for label, x, y in zip(labels, x_values, y_values):
    plt.scatter(x, y, label=label)

# Set plot limits and labels
plt.xlim(-10, 10)
plt.ylim(-10, 10)
plt.title("Political Compass Plot")
plt.xlabel("Economic Left/Right")
plt.ylabel("Social Libertarian/Authoritarian")

# Add grid and legend
plt.grid(color='gray', linestyle='--', linewidth=0.5)
plt.legend(loc='upper left', fontsize=8)  # Show legend with model labels
output_file = os.path.join(directory_path, "political_compass_plot.png")
plt.savefig(output_file, dpi=300, bbox_inches='tight')

# Show the plot
plt.show()