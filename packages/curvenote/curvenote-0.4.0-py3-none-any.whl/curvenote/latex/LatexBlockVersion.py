import logging
from curvenote.latex.utils.index import LocalMarker
from .utils.regex import HREF_COMMAND_OXA_REGEX
from typing import List
from curvenote.latex import utils

from ..client import Session
from ..models import (
    BlockKind,
    BlockVersion,
    VersionID,
)
from . import utils

def skipping_msg(thing: str, version_id: VersionID):
    return (
        f"Caught error trying to localize {thing} for block {str(version_id)}, skipping"
    )


class LatexBlockVersion:
    """
    Class to represent an block in the latex project.
    Encapulates operations applied in processing a block's content including
    calls to fetch content that it encapsulates

    Takes a reference to the reference_list and figure_list and updates these as a side effect
    """

    def __init__(
        self,
        session: Session,
        assets_folder: str,
        reference_list: List[LocalMarker],
        figure_list: List[LocalMarker],
        version: BlockVersion,
    ):
        self.session = session
        self.assets_folder = assets_folder
        self.reference_list = reference_list
        self.figure_list = figure_list
        self.version = version
        self._content = ""

    @property
    def content(self):
        return self._content

    def _localize_images_in_content(self, content: str):
        try:
            return utils.localize_images_from_content_block(
                self.session, self.assets_folder, self.figure_list, content
            )
        except Exception as err:  # pylint: disable=broad-except
            logging.warning(skipping_msg("image", self.version.id))
            logging.warning(str(err))
            return content

    def _localize_references_in_content(self, content: str):
        try:
            return utils.localize_references_from_content_block(
                self.session, self.reference_list, content
            )
        except Exception as err:  # pylint: disable=broad-except
            logging.warning(skipping_msg("reference", self.version.id))
            logging.warning(str(err))
            return content

    def _localize_href_in_content(self, content: str):
        try:
            return utils.localize_hrefs_in_content(self.session.site_url, content)
        except Exception as err:  # pylint: disable=broad-except
            logging.warning(skipping_msg("href", self.version.id))
            logging.warning(str(err))
            return content

    def localize(self):
        content = ""
        kind = self.version.kind
        if kind == BlockKind.content:
            logging.info("Found: Content Block")
            content = self.version.content
            content = self._localize_images_in_content(content)
            content = self._localize_references_in_content(content)
            content = self._localize_href_in_content(content)

        elif kind == BlockKind.output:
            logging.info(
                "Found: Output Block - num outputs: %s", len(self.version.outputs)
            )
            content = utils.localize_images_from_output_block(
                self.assets_folder, self.version
            )
        elif kind == BlockKind.code:
            logging.info("Found: Code Block")
            content = self.version.content
        elif kind == BlockKind.image:
            logging.info("Found: Top Level Image Block")
            content = utils.localize_image_from_top_level_block(
                self.session, self.assets_folder, self.figure_list, self.version
            )
        else:
            logging.warning("Can't process block with kind: %s yet", kind)
            raise ValueError(f"Unknown block kind {kind}")
        self._content = content
