# -*- coding: utf-8 -*-

import click
from . import helpers
from . import split_folder


@click.group()
def main():
    """AI in Dermatology project"""
    pass


@click.command()
def welcome():
    """The main routine."""
    click.echo(click.style('AI in Dermatology project:', bold=True))
    click.echo('Ranked classification of lesions in skin of color with deep neural'
               'networks using transfer learning and patch transformation with'
               'computer vision and GANs')


@click.command()
@click.option('--path', default='data/raw', help='path to raw data')
@click.option('--train_percentage', default=60, help='percentage of train-test split')
@click.option('--output_path', default='data', help='output path for the train-test subdirectories')
def split_raw_data(path: str, train_percentage: int, output_path: str):
    """Split raw data into train and test subdirectories"""
    split_folder.copy_files(path, train_percentage / 100, output_path)


main.add_command(welcome)
main.add_command(split_raw_data)

if __name__ == "__main__":
    main()
