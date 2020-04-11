#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""dermai

Usage:
  dermai gcp project set ([-p | --project] <project-id>) ([-z | --zone] <project-zone>)
  dermai gcp vm start <vm-instance>
  dermai gcp vm stop <vm-instance>
  dermai gcp vm notebook <vm-instance>
  dermai gcp vm connect <vm-instance>
  dermai code split dataset <data_path> <train_percentage> <output_path>
  dermai code train gan <image_dir> <train_steps>
  dermai -h | --help
  dermai --version

Options:
  -h, --help    Show this screen.
  --version     Show version.
"""

from __future__ import unicode_literals, print_function

import os
import sys
import configparser
from docopt import docopt
from invoke import run, exceptions
from subprocess import call, Popen, CalledProcessError
from dermai_impl.dataset_modules import create_dataset
from dermai_impl.gcp_modules import set_gcp_project, start_vm, stop_vm, connect_notebook, connect_ssh

__version__ = "0.1.0"
__author__ = "AI in Dermatology Team"
__license__ = "MIT"


def code_commands(args: dict):
    """Command to train BioMedBert model"""

    # train vocab
    if args['code'] and args['split'] and args['dataset']:
        create_dataset(args['<data_path>'], args['<train_percentage>'], args['<output_path>'])

    # train GAN on image folder
    if args['code'] and args['train'] and args['gan']:
        # change virtualenv
        if not os.path.exists('bigan/venv/'):
            try:
                call(['virtualenv', '--system-site-packages', '-p', 'python3', 'bigan/venv/'])
                run('source bigan/venv/bin/activate')
                call(['pip', 'install', 'tensorflow==1.14'])
                call(['pip', 'install', 'keras==2.2.5'])
            except CalledProcessError:
                print('Bad command')
        else:
            run('source bigan/venv/bin/activate')

        # set image folder
        from bigan import bigan
        bigan.set_directory(args['<image_dir>'])
        bigan.main(int(args['<train_steps>']))

        # deactivate environment
        try:
            run('deactivate')
        except exceptions.UnexpectedExit:
            print('Bad command')


def gcp_commands(args: dict):
    """GCP commands for biomedber CLI."""

    # Configurations
    config = configparser.ConfigParser()

    # setup GCP project
    if args['gcp'] and args['project'] and args['set']:
        # set values
        config.add_section('PROJECT')
        config.set('PROJECT', 'name', args['<project-id>'])
        config.set('PROJECT', 'zone', args['<project-zone>'])

        # write to config file
        with open('./config/gcp_config.ini', 'w') as configfile:
            config.write(configfile)

        # call set project
        set_gcp_project(args['<project-id>'], args['<project-zone>'])

    # start VM
    if args['gcp'] and args['vm'] and args['start']:
        # start vm
        start_vm(args['<vm-instance>'])

    # stop VM
    if args['gcp'] and args['vm'] and args['stop']:
        stop_vm(args['<vm-instance>'])

    # connect VM
    if args['gcp'] and args['vm'] and args['connect']:
        # read configurations
        config.read('config/gcp_config.ini')
        project_id = config['PROJECT']['name']
        zone = config['PROJECT']['zone']

        # ssh to instance
        connect_ssh(project_id, zone, args['<vm-instance>'])

    # launch jupyter notebook on VM
    if args['gcp'] and args['vm'] and args['notebook']:
        # read configurations
        config.read('config/gcp_config.ini')
        project_id = config['PROJECT']['name']
        zone = config['PROJECT']['zone']

        # lauch notebook
        connect_notebook(project_id, zone, args['<vm-instance>'])


def main():
    """Main entry point for the dermai CLI."""
    args = docopt(__doc__, version=__version__,
                  options_first=True)
    # print(args)

    if args['gcp']:
        gcp_commands(args)

    if args['code']:
        code_commands(args)


if __name__ == '__main__':
    main()
