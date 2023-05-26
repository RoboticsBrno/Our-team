import urllib3
import yaml
from pprint import pprint
from urllib import parse
from jinja2 import Environment, FileSystemLoader

# Set the directories
team_file = './team.yaml'
template_folder = './templates'
output_file_html = './team.html'
output_file_md = './team.md'
team_template = 'team_template.jinja2'
image_prefix = "https://raw.githubusercontent.com/RoboticsBrno/Our-team/main/docs/"


# Custom function to remove http:// or https:// from URLs
def nice_url(url):
    url = url.replace('http://', '').replace('https://', '')
    if url.startswith("www."):
        url = url[4:]
    if url.startswith("github.com/"):
        url = url[11:]
    if url.startswith("github.io/"):
        url = url[10:]
    if url.endswith("/"):
        url = url[:-1]
    if url.startswith("linkedin.com/"):
        url = parse.unquote(url[13:])
    return url

def image_absolute_path(image):
    return parse.urljoin(image_prefix, image)

def remove_blank_lines(text):
    lines = text.split('\n')
    non_empty_lines = [line for line in lines if line.strip() != ""]
    return "\n".join(non_empty_lines)


def load_yaml(filename: str) -> dict:
    try :
        with open(filename, 'r') as file:
            # Load the YAML data
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"File {filename} not found")
        exit(1)

def load_team_data(team_filename: str) -> dict:
    return load_yaml(team_filename)

def save_team_portfolio(filename: str, team_portfolio: str) -> None:
    with open(filename, 'w') as file:
        file.write(team_portfolio)

def generate_team_portfolio(team_data: dict, template_folder: str, team_template: str) -> str:
    # Set the template environment
    env = Environment(loader=FileSystemLoader(template_folder))

    # Add the custom function to the template environment
    env.filters['remove_http_s'] = nice_url
    env.filters['image_absolute_path'] = image_absolute_path

    portfolio_string = '<script src="https://kit.fontawesome.com/5b4ac9752d.js" crossorigin="anonymous"></script>\n'

    # Loop through the team members
    for index, team_member_data in enumerate(team_data):
        team_member_data["index"] = index

        # Load the Jinja template
        template = env.get_template(team_template)

        # Render the template with the YAML data
        rendered_text = template.render(team_member_data)

        # Remove blank lines from the rendered text
        cleaned_text = remove_blank_lines(rendered_text)

        # Write the cleaned text to the output file
        portfolio_string += cleaned_text

    return portfolio_string



if __name__ == "__main__":
    team_data = load_team_data(team_file)
    # pprint(team_data)

    portfolio = generate_team_portfolio(team_data, template_folder, team_template)

    save_team_portfolio(output_file_html, portfolio)
    save_team_portfolio(output_file_md, portfolio)

    print("Team portfolio generated successfully.")
