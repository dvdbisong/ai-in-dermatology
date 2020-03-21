# -*- coding: utf-8 -*-

import click
from ml import split_folder


def create_helpers_cli_group():
    """Helper cli group"""
    group = click.Group(name="helper")
    group.add_command(welcome)
    group.add_command(split_raw_data)
    return group


# @click.command(name='print',
#                help='Print a pipeline.\n\n{instructions}'.format(
#                    instructions=get_pipeline_instructions('print'))
#                )

# @click.command(
#     name='graphviz',
#     help=(
#         'Visualize a pipeline using graphviz. Must be installed on your system '
#         '(e.g. homebrew install graphviz on mac). \n\n{instructions}'.format(
#             instructions=get_pipeline_instructions('graphviz')
#         )
#     ),
# )
@click.command(name='welcome')
def welcome():
    """The main routine."""
    click.echo(click.style('AI in Dermatology project:', bold=True))
    click.echo('Ranked classification of lesions in skin of color with deep neural'
               'networks using transfer learning and patch transformation with'
               'computer vision and GANs')


@click.command(name='split')
@click.option('--path', default='data/raw', help='path to raw data')
@click.option('--train_percentage', default=60, help='percentage of train-test split')
@click.option('--output_path', default='data', help='output path for the train-test subdirectories')
def split_raw_data(path: str, train_percentage: int, output_path: str):
    """Split raw data into train and test subdirectories"""
    split_folder.copy_files(path, train_percentage / 100, output_path)


helpers_cli = create_helpers_cli_group()
