import re
from os import path
from typing import Dict, Union
from jinja2 import Environment, PackageLoader, FileSystemLoader


class TemplateRenderer:
    def __init__(self, searchpath: Union[str, None] = None):
        self.jinja = None
        self.package_templates = path.join("latex", "templates", "default")
        if searchpath:
            self.reset_environment(FileSystemLoader(searchpath))
        else:
            self.reset_environment(PackageLoader("curvenote", self.package_templates))

    def reset_environment(self, loader):
        """
        Define our own custom jinja environment that plays nicely with LaTeX

        [# #] - blocks
        [[ ]] - variables
        ## ## - comments

        disabled line statements

        """
        self.jinja = Environment(
            block_start_string=r"[#",
            block_end_string="#]",
            variable_start_string=r"[[",
            variable_end_string="]]",
            comment_start_string=r"%#",
            comment_end_string="#%",
            trim_blocks=True,
            autoescape=False,
            auto_reload=True,
            loader=loader,
        )
        self.jinja.globals.update(__builtins__)

    def use_from_folder(self, searchpath: str):
        """
        Load templates from file system
        """
        self.reset_environment(FileSystemLoader(searchpath))

    def use_basic_template(self):
        """
        Load the basic template (fallback) included in the package
        """
        self.reset_environment(PackageLoader("curvenote", self.package_templates))

    def render_from_string(self, template: str, data: Dict):
        """
        Render using the template specified in a string
        """
        template = self.jinja.from_string(template, data)
        return template.render()

    def list_templates(self):
        return [t for t in self.jinja.list_templates() if re.match(r".*.tex$", t)]

    def render(self, data: Dict, template_name: str = "template.tex"):
        """
        A render method which will
        """
        template = self.jinja.get_template(template_name)
        return template.render(**data)
