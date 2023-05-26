import os
import yaml
from jinja2 import Environment, FileSystemLoader

# Set the directories
team_folder = './team'
template_folder = './templates'
output_file = './output.html'
team_template = 'team_template.jinja2'

config = {}
with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

# Custom function to remove http:// or https:// from URLs
def remove_http_s(url):
    return url.replace('http://', '').replace('https://', '')

def image_absolute_path(image):
    return config['image_base_url'] + image

# Function to remove blank lines from text
def remove_blank_lines(text):
    lines = text.split('\n')
    non_empty_lines = [line for line in lines if line.strip() != ""]
    return "\n".join(non_empty_lines)

# Set the template environment
env = Environment(loader=FileSystemLoader(template_folder))

# Add the custom function to the template environment
env.filters['remove_http_s'] = remove_http_s
env.filters['image_absolute_path'] = image_absolute_path

# Get the list of .yaml files
yaml_files = [f for f in os.listdir(team_folder) if f.endswith('.yaml')]

# Open the output file
with open(output_file, 'w') as outfile:
    outfile.write('<script src="https://kit.fontawesome.com/5b4ac9752d.js" crossorigin="anonymous"></script>\n')
    # Loop through the YAML files
    index = 0
    for yaml_file in yaml_files:
        # Open the YAML file
        if yaml_file == 'template.yaml':
            continue

        with open(os.path.join(team_folder, yaml_file), 'r') as yf:
            # Load the YAML data
            data = yaml.safe_load(yf)
            data["Index"] = index + 1
            index += 1

            # Load the Jinja template
            template = env.get_template(team_template)

            # Render the template with the YAML data
            rendered_text = template.render(data)

            # Remove blank lines from the rendered text
            cleaned_text = remove_blank_lines(rendered_text)

            # Write the cleaned text to the output file
            outfile.write(cleaned_text)

print(f"All data has been written to {output_file}")