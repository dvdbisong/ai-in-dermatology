#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import click
import webbrowser
from invoke import run, exceptions
from subprocess import call, Popen, CalledProcessError


def create_gpu(name: str, zone: str, image_family: str, accelerator: str, machine_type: str):
    """Provision a Deep Learning VM instance with one or more GPUs"""
    try:
        click.echo('Creating GPU instance {}'.format(name))
        call(['bash', './bash/create_deep_vm.sh', name, zone, image_family, accelerator, machine_type])
    except CalledProcessError:
        print('Cannot create GPU')


def connect_ssh(project_id: str, zone: str, vm_instance: str):
    """SSH into VM"""
    try:
        call(['gcloud', 'compute', 'ssh', '--zone', zone, vm_instance, '--project', project_id])
    except CalledProcessError:
        print('Bad command')


def connect_notebook(name: str, zone: str, project_id: str):
    """Connect to JupyterLab on AI Platform Deep Learning VM Image instance"""

    process = Popen(['nohup', 'bash', './bash/connect_jupyterlab.sh', name, zone, project_id],
                    stdout=open('/dev/null', 'w'),
                    stderr=open('logfile.log', 'a'),
                    preexec_fn=os.setpgrp
                    )

    if process.returncode is None:
        click.echo('Connecting to Jupyterlab at http://localhost:8080')
        webbrowser.open('http://localhost:8080')


def stop_vm(name: str, zone: str):
    """Stop deep learning VM instance on GCP"""
    try:
        click.echo('Stopping instance {}'.format(name))
        call(['gcloud', 'compute', 'instances', 'stop', name, '--zone', zone])
    except CalledProcessError:
        print('Cannot stop VM')


def start_vm(name: str, zone: str):
    """Start deep learning VM instance on GCP"""
    try:
        click.echo('Starting instance {}'.format(name))
        call(['gcloud', 'compute', 'instances', 'start', name, '--zone', zone])
    except CalledProcessError:
        print('Cannot start VM')


def upload_bucket(source_dir: str, bucket_name: str):
    """Upload data to GCP storage bucket"""
    click.echo('Uploading source folder: "{}" to storage bucket: "{}"'.format(source_dir, bucket_name))
    try:
        call(['gsutil', '-m', 'cp', '-R', source_dir, 'gs://{}'.format(bucket_name)])
    except CalledProcessError:
        print('Bucket {} not found'.format(bucket_name))


def create_bucket(name: str):
    """Create GCP storage bucket"""
    try:
        click.echo('Creating bucket: "{}"'.format(name))
        call(['gsutil', 'mb', 'gs://{}/'.format(name)])
    except CalledProcessError:
        print('Cannot create bucket')


def list_bucket(name: str):
    """List content of GCP storage bucket"""
    try:
        click.echo('Listing content for bucket: "{}"'.format(name))
        call(['gsutil', 'ls', 'gs://{}/'.format(name)])
    except CalledProcessError:
        print('Cannot list bucket')


def list_vms():
    """List compute VMs on GCP"""
    try:
        call(['bash', './bash/show_compute_vms.sh'])
    except CalledProcessError:
        print('Cannot list bucket')


def set_gcp_project(project_id: str, zone: str):
    """Set GCP project ID"""
    try:
        run('gcloud config set project {}'.format(project_id))
        run('gcloud config set compute/zone {}'.format(zone))
    except exceptions.UnexpectedExit:
        print('Bad command')
