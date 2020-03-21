# -*- coding: utf-8 -*-

import os
import click
import webbrowser
from subprocess import call, Popen
from google.cloud import storage


def create_gcp_cli_group():
    """GCP helper scripts"""
    # set Environment Credentials
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'SA-ai-in-derm.json'

    group = click.Group(name='gcp')
    group.add_command(create_gpu)
    group.add_command(connect)
    group.add_command(list_vms)
    group.add_command(stop_gpu)
    group.add_command(start_gpu)
    group.add_command(upload_bucket)
    group.add_command(create_bucket)
    group.add_command(list_bucket)
    return group


# Parameters
# TODO: Work on passing context between commands


@click.command(name='gpu_create')
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


@click.command(name='notebook_connect')
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


@click.command(name='gpu_stop')
@click.option('--name', default='ai-derm-tf2-2-0-cu100', help='name of GPU instance')
@click.option('--zone', default='us-west1-b', help='compute zone')
def stop_gpu(name: str, zone: str):
    """Stop GPU deep learning VM instance on GCP"""
    click.echo('Stopping GPU instance {}'.format(name))
    call(['gcloud', 'compute', 'instances', 'stop', name, '--zone', zone])


@click.command(name='gpu_start')
@click.option('--name', default='ai-derm-tf2-2-0-cu100', help='name of GPU instance')
@click.option('--zone', default='us-west1-b', help='compute zone')
def start_gpu(name: str, zone: str):
    """Start GPU deep learning VM instance on GCP"""
    click.echo('Starting GPU instance {}'.format(name))
    call(['gcloud', 'compute', 'instances', 'start', name, '--zone', zone])


@click.command(name='bucket_upload')
@click.option('--source_dir', help='source folder')
@click.option('--bucket_name', default='ai-in-dermatology', help='storage bucket')
def upload_bucket(source_dir: str, bucket_name: str):
    """Upload data to GCP storage bucket"""
    click.echo('Uploading source folder: "{}" to storage bucket: "{}"'.format(source_dir, bucket_name))
    # Instantiates a client
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    if bucket.exists():
        call(['gsutil', '-m', 'cp', '-R', source_dir, 'gs://{}'.format(bucket_name)])
    else:
        click.echo(click.style('Bucket Not Found', bold=True))


@click.command(name='bucket_create')
@click.option('--name', help='storage bucket')
def create_bucket(name: str):
    """Create GCP storage bucket"""
    click.echo('Creating bucket: "{}"'.format(name))
    call(['gsutil', 'mb', 'gs://{}/'.format(name)])


@click.command(name='bucket_list')
@click.option('--name', default='ai-in-dermatology', help='storage bucket')
def list_bucket(name: str):
    """List content of GCP storage bucket"""
    click.echo('Listing content for bucket: "{}"'.format(name))
    call(['gsutil', 'ls', 'gs://{}/'.format(name)])


@click.command(name='vm_list')
def list_vms():
    """List compute VMs on GCP"""
    call(['bash', './bash/show_compute_vms.sh'])


gcp_cli = create_gcp_cli_group()
