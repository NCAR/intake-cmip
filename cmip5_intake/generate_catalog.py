#!/usr/bin/env python
"""
The main command line script. This is the script that is
executed to generate an intake catalog.
"""
import click
import yaml 
from jinja2 import Environment, FileSystemLoader
from pathlib import Path 
import os 


@click.command()
@click.option(
    "--config-data-file",
    default=None,
    type=click.Path(exists=True, resolve_path=True),
    show_default=True,
    help="Configuration file containing data to feed in a jinja template",
)
@click.option(
    "--template-file",
    default=None,
    type=click.Path(exists=True, resolve_path=True),
    show_default=True,
    help="Template file"
)
def generator(config_data_file, template_file):
    # Load data from YAML into Python dictionary
    config_data = yaml.load(open(config_data_file))
 
    # Load Jinja2 template
    template_dir = os.path.dirname(os.path.abspath(template_file))

    env = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True, lstrip_blocks=True)

    template = env.get_template(os.path.basename(template_file))


    # Render the template with data and stream it to an output file
    template.stream(config_data).dump('catalog.yaml')

if __name__ == "__main__":
    generator()