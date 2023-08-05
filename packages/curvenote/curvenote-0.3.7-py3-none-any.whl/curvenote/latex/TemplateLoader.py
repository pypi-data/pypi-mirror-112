from pydantic.errors import PathError
from curvenote.models import BlockFormat
import logging
import os
import yaml
import pkg_resources
from typing import Optional, Dict
from enum import Enum
from zipfile import ZipFile
from shutil import copyfile
from distutils.dir_util import copy_tree
from .TemplateRenderer import TemplateRenderer
from .TemplateOptions import TemplateOptions
from ..utils import download
from ..client import Session
from .DefBuilder import DefBuilder


class TemplateLoader:
    def __init__(self, target_folder: str):
        self.template_name = None
        self.renderer = None
        self.options = None

        self.target_folder = target_folder
        os.makedirs(self.target_folder, exist_ok=True)

    def initialise_with_default(self):
        logging.info("TemplateLoader - Initialising with default template")
        logging.info("Copying template assets")
        template_location = pkg_resources.resource_filename(
            "curvenote", os.path.join("latex", "templates", "default")
        )
        template_assets = ["curvenote.png", "template.yml"]
        for asset_filename in template_assets:
            src = os.path.join(template_location, asset_filename)
            dest = os.path.join(self.target_folder, asset_filename)
            logging.info("Copying: %s to %s", src, dest)
            copyfile(src, dest)

        self.template_name = "default"
        self.renderer = TemplateRenderer()
        self.options = TemplateOptions()

    def initialise_from_path(self, local_template_path: str):
        logging.info("Using local template found at: %s", local_template_path)

        abs_path = os.path.abspath(os.path.expanduser(local_template_path))

        if not os.path.exists(abs_path):
            raise ValueError('local template path does not exist')

        if not os.path.isdir(abs_path):
            raise ValueError('local template path must point to a folder')

        try:
            copy_tree(abs_path, self.target_folder)
        except Exception as err:
            logging.error("Could not copy local template from %s to %s", abs_path, self.target_folder)
            logging.error(str(err))
            raise err

        self.template_name = os.path.basename(os.path.normpath(abs_path))
        self.renderer = TemplateRenderer()
        self.renderer.use_from_folder(self.target_folder)
        self.options = TemplateOptions(self.target_folder)

    def initialise_from_template(self, session: Session, template_name: str):
        logging.info("Writing to target folder: %s", self.target_folder)

        logging.info("Looking up template %s", template_name)
        try:
            link = session.get_template_download_link(template_name)
        except ValueError as err:
            logging.error("could not download template %s", template_name)
            raise ValueError(f"could not download template: {template_name}") from err

        # fetch template to local folder
        logging.info("Found template, downloading...")
        zip_filename = os.path.join(self.target_folder, f"{template_name}.template.zip")
        download(link, zip_filename)

        # unzip
        logging.info("Download complete, unzipping...")
        with ZipFile(zip_filename, "r") as zip_file:
            zip_file.extractall(self.target_folder)
        logging.info("Unzipped to %s", self.target_folder)
        os.remove(zip_filename)
        logging.info("Removed %s", zip_filename)

        # success -- update members
        self.template_name = template_name
        self.renderer = TemplateRenderer()
        self.renderer.use_from_folder(self.target_folder)
        self.options = TemplateOptions(self.target_folder)

    def set_user_options_from_yml(self, user_options_path: str):
        if self.options is None:
            raise ValueError('TemplateLoader not initialized')

        with open(user_options_path, "r") as file:
            self.options.set_user_options(yaml.load(file, Loader=yaml.FullLoader))

    def set_user_options(self, user_options: Dict):
        if self.options is None:
            raise ValueError('TemplateLoader not initialized')
        self.options.set_user_options(user_options)

    def build_defs(self):
        """
        TODO: regsiter schema options here with:
            - template config path
            - a map of:
                - paths to definitions for known options
                - package dependencies for known options

        1. iterate over all *registered* schema options
            1.1 check if option is speced in the template, using the template setting or
                using the default
            1.2 log any package dependencied in the package listing
        """
        if self.template_name is None or self.options is None:
            raise ValueError("TemplateLoader has not been initialized")
        def_builder = DefBuilder()
        def_builder.build(self.options, self.target_folder)
