from curvenote.models import BlockFormat
import logging
import os
import yaml
import pkg_resources
from typing import Optional, Dict
from enum import Enum
from zipfile import ZipFile
from shutil import copyfile
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
        with open(user_options_path, "r") as file:
            self.options.parse_user_optons(yaml.load(file, Loader=yaml.FullLoader))

    def set_user_options(self, user_options: Dict):
        self.options.parse_user_option(user_options)

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
        if self.template_name is None:
            raise ValueError("TemplateLoader has not been initialized")
        def_builder = DefBuilder()
        def_builder.build(self.options, self.target_folder)
