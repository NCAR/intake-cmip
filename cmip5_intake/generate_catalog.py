import yaml 
from jinja2 import Environment, FileSystemLoader
from pathlib import Path 
import os 

def generator(config_data_file_path, template_file_path):
    # Load data from YAML into Python dictionary
    config_data = yaml.load(open(config_data_file_path))
 
    # Load Jinja2 template
    template_dir = os.path.dirname(os.path.abspath(template_file_path))

    env = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True, lstrip_blocks=True)

    template = env.get_template(os.path.basename(template_file_path))


    # Render the template with data and stream it to an output file
    template.stream(config_data).dump('catalog.yml')
