import os
import logging
from .TemplateLoader import TemplateLoader
from curvenote.latex.utils.decorators import log_and_raise_errors
from typing import Union, List, NamedTuple
from pydantic import BaseModel
from curvenote.models import BlockFormat, Project
from ..client import Session
from ..utils import decode_url, decode_oxa_link
from .LatexArticle import LatexArticle
from .utils.index import LocalMarker


logger = logging.getLogger()


class ProjectItem(NamedTuple):
    path: str
    filename: str
    item: LatexArticle


class TemplateOptions(BaseModel):
    compact: bool = True


class LatexProjectBuilder:
    def __init__(self, loader: TemplateLoader, session: Session, target_folder: str):
        self.loader = loader
        self.session = session

        self.target_folder = os.path.abspath(target_folder)
        self.assets_folder = os.path.join(self.target_folder, "assets")
        self.images_folder = os.path.join(self.target_folder, "assets", "images")
        self.documents_folder = os.path.join(self.target_folder, "documents")

        logger.info("Creating %s", self.images_folder)
        os.makedirs(self.images_folder, exist_ok=True)
        logger.info("Creating %s", self.documents_folder)
        os.makedirs(self.documents_folder, exist_ok=True)

        self.articles: List[ProjectItem] = []
        self.reference_list: List[LocalMarker] = []
        self.figure_list: List[LocalMarker] = []

    @classmethod
    def build_single_article_by_name(
        cls,
        loader: TemplateLoader,
        session: Session,
        project_id_or_obj: Union[str, Project],
        article_id: str,
        version: int,
    ):
        latex_project = cls(loader, session, loader.target_folder)
        latex_project.add_article(
            project_id_or_obj, article_id, version, loader.options.tex_format
        )
        latex_project.reconcile()
        latex_project.write()

    @classmethod
    def build_single_article_by_url(
        cls, loader: TemplateLoader, session: Session, url: str
    ):
        vid, pathspec = None, None
        try:
            vid = decode_oxa_link(url)
        except ValueError:
            pathspec = decode_url(url)

        latex_project = cls(loader, session, loader.target_folder)

        logging.info("writing to %s", {latex_project.target_folder})
        latex_project.create_folders(loader.options.compact)

        if vid:
            latex_project.add_article(
                vid.project, vid.block, vid.version, loader.options.tex_format
            )
        else:
            if not pathspec.block:
                raise ValueError("URL does not include a block id")
            latex_project.add_article(
                pathspec.project,
                pathspec.block,
                pathspec.version,
                loader.options.tex_format,
            )

        latex_project.reconcile()
        latex_project.write()

    def create_folders(self, compact: bool = True):
        logger.info("Creating %s", self.images_folder)
        os.makedirs(self.images_folder, exist_ok=True)

        if not compact:
            logger.info("Creating %s", self.documents_folder)
            os.makedirs(self.documents_folder, exist_ok=True)

    def next_index(self):
        return len(self.articles)

    @log_and_raise_errors(lambda *args: "Could not add article to LaTeX project")
    def add_article(
        self,
        project_id: Union[str, Project],
        article_id: str,
        version: int,
        fmt: BlockFormat,
    ):
        logging.info("adding article using ids/names")
        latex_article = LatexArticle(self.session, project_id, article_id)
        latex_article.fetch(fmt, version)
        latex_article.localize(
            self.session, self.assets_folder, self.reference_list, self.figure_list
        )
        filename = f"{self.next_index()}_{latex_article.block.name}"
        self.articles.append(
            ProjectItem(
                path=f"documents/{filename}", item=latex_article, filename=filename
            )
        )
        logging.info("added article")

    def reconcile(self):
        for article in self.articles:
            article.item.reconcile_figures(self.figure_list)

    def render(self):
        logging.info("Rendering template...")

        if len(self.articles) < 1:
            raise ValueError("Need at least one article")

        content = ""
        for article in self.articles:
            content += article.item.content

        first = self.articles[0]

        letters = 'abcdefghijklmnopqrstuvwxyz'
        data = dict(
            doc=dict(
                oxalink=first.item.oxalink(self.session.site_url),
                title=first.item.title,
                authors=[
                    dict(
                        username='curvenote',
                        name=name,
                        affiliation='',
                        letter=letters[i]
                        ) for i, name in enumerate(first.item.author_names)],
                date=first.item.date,
                tags=['keyword1', 'keyword2', 'keyword3']
            ),
            tagged=dict(),
            curvenote=dict(defs=r"\input{curvenote.def}"),
            options=dict(docclass=''),
            CONTENT=content,
        )

        return self.loader.renderer.render(data)

    @log_and_raise_errors(lambda *args: "Could not write final document")
    def write(self):
        logging.info("ProjectBuilder - writing...")

        logging.info("Building template defs")
        self.loader.build_defs()

        if not self.loader.options.compact:
            for article in self.articles:
                article_filepath = os.path.join(
                    self.documents_folder, article.filename + ".tex"
                )
                article.item.write(article_filepath)

        content = self.render()

        logging.info("Writing index.tex...")
        with open(os.path.join(self.target_folder, "index.tex"), "w+") as file:
            file.write(content)

        logging.info("Writing main.bib...")
        if len(self.reference_list) > 0:
            with open(os.path.join(self.target_folder, "main.bib"), "w+") as file:
                for reference in self.reference_list:
                    file.write(f"{reference.content}\n")

        logging.info("Done!")
