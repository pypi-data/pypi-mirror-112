from curvenote.latex.schema.RaggedBottomOption import RaggedBottomSchemaOption
from curvenote.latex.schema import (
    CalloutSchemaOption,
    CodeSchemaOption,
    HideLinksSchemaOption,
    SloppySchemaOption,
    StringSchemaOption,
)
import os
import logging
import pkg_resources
from .utils.decorators import just_log_errors, log_and_raise_errors
from .TemplateOptions import TemplateOptions
from .schema.AsideSchemaOption import AsideSchemaOption
from typing import Dict


def get_def_file_path(filename: str):
    def_path = pkg_resources.resource_filename("curvenote", "latex/templates/defs")
    return os.path.join(def_path, filename)


def get_def_template_file_path(template_location: str, filename: str):
    return os.path.join(template_location, filename)


@just_log_errors(lambda *args: f"Could not open def file at {args[0]}, skipping...")
def get_def_from_pkg(filename: str):
    with open(get_def_file_path(filename), "r") as file:
        return file.read()


@just_log_errors(lambda *args: f"Could not open def file at {args[0]}, skipping...")
def read_from_file(fullpath: str):
    with open(fullpath, "r") as file:
        return file.read()


class DefBuilder:

    schema_options: Dict
    defs_path: str

    def __init__(self):
        """
        All schema options should be registered here
        """
        self.schema_options: Dict[str, StringSchemaOption] = {}

        self.schema_options["aside"] = AsideSchemaOption()
        self.schema_options["callout"] = CalloutSchemaOption()
        self.schema_options["code"] = CodeSchemaOption()
        self.schema_options["raggedbottom"] = RaggedBottomSchemaOption()
        self.schema_options["sloppy"] = SloppySchemaOption()
        self.schema_options["hidelinks"] = HideLinksSchemaOption()

    def build(self, options: TemplateOptions, target_path: str):
        def_paths = self.compose(options)
        def_contents = self.serialize(*def_paths)
        self.write(target_path, *def_contents)

    def compose(self, template_options: TemplateOptions):
        logging.info("DefBuilder.compose")
        passopts_paths = []
        packages_paths = []
        setup_paths = []

        # iterate over registered options, check to see if the
        # option has been set in the template options, if not
        # use the default
        logging.info("Iterating over %s options", len(self.schema_options))
        for name, schema_option in self.schema_options.items():
            logging.info("Checking option %s", name)
            if name in template_options.schema:
                template_setting = template_options.schema[name]
                defs = schema_option.get(template_setting)
                logging.info("%s - using template option: %s", name, template_setting)
            else:
                defs = schema_option.get()  # default
                logging.info(
                    "%s - using schema default option: %s", name, schema_option.default
                )

            if len(defs.passopts) > 0:
                for passopt in defs.passopts:
                    passopts_paths.append(get_def_file_path(passopt))
            if len(defs.packages) > 0:
                for package in defs.packages:
                    packages_paths.append(get_def_file_path(package))
            if len(defs.setup) > 0:
                for setup in defs.setup:
                    full_path = (
                        get_def_template_file_path(
                            template_options.template_location, setup
                        )
                        if defs.in_template
                        else get_def_file_path(setup)
                    )
                    setup_paths.append(full_path)

        # dedupe - don't care about ordering
        passopts_paths = list(set(passopts_paths))
        packages_paths = list(set(packages_paths))
        setup_paths = list(set(setup_paths))

        logging.info("passopts %s\n", passopts_paths)
        logging.info("packages %s\n", packages_paths)
        logging.info("setup %s\n", setup_paths)

        # log any option specified in the template that are
        # not supported by a registered schema option here
        for name, template_setting in template_options.schema.items():
            if name not in self.schema_options:
                logging.warning("Unknown schema option %s, skipping...", name)

        return passopts_paths, packages_paths, setup_paths

    def serialize(self, passopts_paths, packages_paths, setup_paths):
        """
        Load defs from files and concatenate
        """

        # base configuration
        base_passopts = get_def_from_pkg("passopts-base.def")
        base_packages = get_def_from_pkg("package-base.def")
        base_setup = get_def_from_pkg("setup-base.def")

        # read contents from def files
        passopts_paths = [read_from_file(p) for p in passopts_paths]
        packages_paths = [read_from_file(p) for p in packages_paths]
        setup_paths = [read_from_file(s) for s in setup_paths]

        newline = "\n"
        passopts = f"% Pass Options Section\n% base\n{base_passopts}\n% template\n{newline.join(passopts_paths)}\n"
        packages = f"% Use Package Section\n% base\n{base_packages}\n% template\n{newline.join(packages_paths)}\n"
        setup = f"% Setup Section\n% base\n{base_setup}\n% template\n{newline.join(setup_paths)}\n"

        return passopts, packages, setup

    @log_and_raise_errors(lambda *args: f"Could not write defs to: {args[0]}")
    def write(self, target_path: str, passopts: str, packages: str, setup: str):
        with open(
            os.path.join(target_path, "curvenote.passopts.def"), "w"
        ) as defs_file:
            defs_file.write(passopts)
        with open(
            os.path.join(target_path, "curvenote.packages.def"), "w"
        ) as defs_file:
            defs_file.write(packages)
        with open(os.path.join(target_path, "curvenote.setup.def"), "w") as defs_file:
            defs_file.write(setup)
        with open(os.path.join(target_path, "curvenote.def"), "w") as defs_file:
            defs_file.write(
                "% Start Curvenote Definitions\n\\input{curvenote.passopts.def}\n"
                "\\input{curvenote.packages.def}\n\\input{curvenote.setup.def}\n% End Curvenote Definitions\n"
            )
