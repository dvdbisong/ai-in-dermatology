# -*- coding: utf-8 -*-

import os
import sys
import click
from version import __version__
from .gcp import gcp_cli
from .helpers import helpers_cli


def create_main_cli():
    """Commands for AI in Dermatology project"""
    commands = {
        'helpers': helpers_cli,
        'gcp': gcp_cli,
    }

    @click.group(commands=commands)
    @click.version_option(version=__version__)
    def group():
        """CLI tools for working with AI in Dermatology research."""

    # add the path for the cwd so imports in dynamically loaded code work correctly
    sys.path.append(os.getcwd())
    return group


cli = create_main_cli()


def main():
    """Entry point for console application"""
    cli(obj={})  # pylint:disable=E1123
