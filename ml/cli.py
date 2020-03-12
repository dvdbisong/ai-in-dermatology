# -*- coding: utf-8 -*-


import os
import click
import webbrowser
from . import helpers
from . import split_folder
from subprocess import call, Popen


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


@click.command()
@click.option('--name', default='ai-derm-tf2-2-0-cu100', help='name of GPU instance')
@click.option('--zone', default='us-west1-b', help='compute zone')
@click.option('--image_family', default='tf2-2-0-cu100', help='must be one of the GPU-specific image types')
@click.option('--accelerator', default='type=nvidia-tesla-k80,count=8', help='specifies the GPU type to use. Must be '
                                                                             'specified in the format '
                                                                             '--accelerator="type=TYPE,count=COUNT"')
def create_gpu(name: str, zone: str, image_family: str, accelerator: str):
    """Provision a Deep Learning VM instance with one or more GPUs"""
    click.echo('Creating GPU instance {}'.format(name))
    call(['bash', './bash/create_deep_vm.sh', name, zone, image_family, accelerator])


@click.command()
@click.option('--name', default='ai-derm-tf2-2-0-cu100', help='name of GPU instance')
@click.option('--zone', default='us-west1-b', help='compute zone')
@click.option('--project_id', default='ekabasandbox', help='GCP project ID')
def connect(name: str, zone: str, project_id: str):
    """Connect to JupyterLab on AI Platform Deep Learning VM Image instance"""

    process = Popen(['nohup', 'bash', './bash/connect_jupyterlab.sh', name, zone, project_id],
                    stdout=open('/dev/null', 'w'),
                    stderr=open('logfile.log', 'a'),
                    preexec_fn=os.setpgrp
                    )

    if process.returncode is None:
        click.echo('Connecting to Jupyterlab at http://localhost:8080')
        webbrowser.open('http://localhost:8080')


@click.command()
@click.option('--name', default='ai-derm-tf2-2-0-cu100', help='name of GPU instance')
@click.option('--zone', default='us-west1-b', help='compute zone')
def stop_gpu(name: str, zone: str):
    """Stop GPU deep learning VM instance on GCP"""
    click.echo('Stopping GPU instance {}'.format(name))
    call(['gcloud', 'compute', 'instances', 'stop', name, '--zone', zone])


@click.command()
@click.option('--name', default='ai-derm-tf2-2-0-cu100', help='name of GPU instance')
@click.option('--zone', default='us-west1-b', help='compute zone')
def start_gpu(name: str, zone: str):
    """Start GPU deep learning VM instance on GCP"""
    click.echo('Starting GPU instance {}'.format(name))
    call(['gcloud', 'compute', 'instances', 'start', name, '--zone', zone])


@click.command()
def list_vms():
    """List compute VMs on GCP"""
    call(['bash', './bash/show_compute_vms.sh'])


main.add_command(split_raw_data)
main.add_command(create_gpu)
main.add_command(connect)
main.add_command(list_vms)
main.add_command(stop_gpu)
main.add_command(start_gpu)

if __name__ == "__main__":
    main()
