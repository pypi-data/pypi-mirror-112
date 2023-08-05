from curvenote.models import BlockFormat
import os
import pkg_resources
import logging
from typing import Dict, Any
from pykwalify.core import Core as YamlSchema
import yaml


TEMPLATES_PATH = pkg_resources.resource_filename("curvenote", "latex/templates")
DEFAULT_TEMPLATE_PATH = os.path.join(TEMPLATES_PATH, "default")


class TemplateOptions:
    _tex_format: BlockFormat

    def __init__(self, template_location: str = DEFAULT_TEMPLATE_PATH):
        self.template_schema = None
        self.schemas = [
            os.path.join(TEMPLATES_PATH, "config.schema.yml"),
            os.path.join(TEMPLATES_PATH, "template.schema.yml"),
        ]

        self.template_location = template_location
        template_yml = os.path.join(template_location, "template.yml")
        print("Looking for template on %s", template_yml)
        if not os.path.exists(template_yml):
            logging.info("%s does not exist", template_yml)
            raise FileNotFoundError(f"{template_yml} does not exist")

        self.template_schema = YamlSchema(
            source_file=template_yml, schema_files=self.schemas
        )
        self.template_schema.validate(raise_exception=True)
        self.flat_config = TemplateOptions._flatter(
            self.template_schema.source["config"]
        )
        self._tex_format = (
            BlockFormat.tex
            if self.get("config.build.vanilla")
            else BlockFormat.tex_curvenote
        )

    @property
    def tex_format(self):
        return self._tex_format

    def __len__(self):
        if self.template_schema is None:
            return 0
        return len(self.flat_config)

    def get(self, path: str, default: Any = None):
        """
        Get a value from the template options on the specified path

        raises a ValueError if the options is not found
        """
        try:
            return TemplateOptions.find(path, self.template_schema.source)
        except KeyError:
            return default

    def dumps(self):
        """
        Dump the template options as a YAML string
        """
        return yaml.dump(self.template_schema.source)

    @staticmethod
    def _flatter(options):
        """
        single level flattening and path concatenation
        """
        flat = []
        for top, group in options.items():
            for k, value in group.items():
                flat.append((f"{top}.{k}", value))
        return flat

    @staticmethod
    def find(element: str, data: Dict):
        keys = element.split(".")
        rv = data
        for key in keys:
            if key not in rv:
                raise KeyError(f"{key} not found")
            rv = rv[key]
        return rv

    @staticmethod
    def templates_path():
        return TEMPLATES_PATH

    def set_user_options(self, user_options: Dict):
        """
        Parse a dict of user options, validate these against the template and
        register any valid options.

        Discard any option not listed in or conforming to the template config.options section
        """

        # TODO register user defined options
        pass

    @property
    def compact(self):
        return self.get("config.build.layout") == "compact"

    @property
    def schema(self):
        """
        Return the schema secton
        """
        return (
            self.template_schema.source["config"]["schema"]
            if self.template_schema
            else None
        )

    @property
    def tagged(self):
        """
        Return the tagged section
        """
        return (
            self.template_schema.source["config"]["tagged"]
            if self.template_schema
            else None
        )

    @property
    def user_options(self):
        """
        TODO
        """
        return (
            self.template_schema.source["config"]["options"]
            if self.template_schema
            else None
        )
