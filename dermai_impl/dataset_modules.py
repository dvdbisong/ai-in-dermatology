#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import click
import shutil


def create_dataset(raw_path, train_percentage, output_path):
    """Move files into subdirectories.

       Iterate through the sub-folders in the raw data directory (data/raw).
       Copy 60% of the images in each sub-folder into the train directory and the remaining into test.
       The train and test directory paths are as listed:
       - data/train/sub-folder
       - data/test/sub-folder

       Args:
           raw_path (string): Path to raw data directory.
           train_percentage (int): Percentage of train-test split.
           output_path (string): Output path for the train-test subdirectories.

       Returns:
           The partitioning of images into training and test fodlers for each directory sub-folder.
    """

    if not os.path.isdir(raw_path):
        click.echo(click.style('Source directory (--path) not found', bold=True))
        raise SystemExit()

    directory = [f for f in os.listdir(raw_path) if os.path.isdir(os.path.join(raw_path, f))]

    with click.progressbar(directory) as bar:
        for raw_data in bar:
            images = [f for f in os.listdir(os.path.join(raw_path, raw_data))
                      if os.path.isfile(os.path.join(os.path.join(raw_path, raw_data), f))]

            # split images into train and test lists
            train_images = images[:int(len(images) * train_percentage)]
            test_images = images[int(len(images) * train_percentage):]

            # assign images to appropriate directories
            image_dict = {'train': train_images,
                          'test': test_images}

            for f_name, f_list in image_dict.items():
                folder_name = f_name

                for image in f_list:
                    new_path = os.path.join(output_path, folder_name, raw_data)
                    if not os.path.exists(new_path):
                        os.makedirs(new_path)

                    old_image_path = os.path.join(os.path.join(raw_path, raw_data), image)
                    new_image_path = os.path.join(new_path, image)
                    shutil.copy(old_image_path, new_image_path)
