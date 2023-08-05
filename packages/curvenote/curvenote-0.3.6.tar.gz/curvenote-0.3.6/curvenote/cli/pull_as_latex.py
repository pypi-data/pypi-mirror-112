import logging
import sys
import typer
import os
from curvenote.utils import decode_oxa_link, decode_url
from ..client import Session
from ..latex import LatexProjectBuilder, TemplateLoader


app = typer.Typer()

logger = logging.getLogger()


def url_set(ctx: typer.Context, value: str):
    if ctx.resilient_parsing:
        return
    if value:
        typer.echo("URL provided project, article and version options will be ignored")
    return value


def pull_as_latex(
    target: str = typer.Argument(
        ...,
        help=(
            "Local folder in which to construct the Latex assets. If TARGET exists it"
            "and all files will be removed and a new empty folder structure created"
        ),
    ),
    token: str = typer.Argument(
        ..., envvar="CURVENOTE_TOKEN", help="API token generated from curvenote.com"
    ),
    url: str = typer.Option(
        None,
        help=("A valid url (or oxa link) to the existing Article"),
        is_eager=True,
        callback=url_set,
    ),
    project: str = typer.Option(
        None,
        help=(
            "Identifier of existing Project containing ARTICLE. PROJECT may match title,"
            " name, or id of an existing Project. If no existing Project is found, an "
            "error will be raised"
        ),
    ),
    article: str = typer.Option(
        None,
        help=(
            "Identifier of existing Article. ARTICLE may match title, name, or id "
            "of an existing Article. If no existing Article is found, an error will"
            "be raised."
        ),
    ),
    version: int = typer.Option(
        None,  # optional
        help=(
            "Version of the article to pull, if not specified will pull the latest version."
        ),
    ),
    template: str = typer.Option(
        None,
        help=("Id (name) of the LaTeX template to apply"),
    ),
    user_options: str = typer.Option(
        None,
        help=(
            "A path to a local YAML file containing user options to apply to the tempalte."
        ),
    ),
):
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    if not url:
        if not project or not article:
            typer.echo("Either a --url or a --project and --article must be specified")
            raise typer.Exit(code=1)

    if user_options is not None and not os.path.exists(user_options):
        typer.echo(f"User options file note found on path {user_options}")
        raise typer.Exit(code=1)

    try:
        session = Session(token)
    except Exception as err:
        typer.echo("Could not start an API session - check your token")
        raise typer.Exit(code=1)

    loader = TemplateLoader(target)
    if template is not None:
        typer.echo(f"Using template: {template}")
        loader.initialise_from_template(session, template)
        if user_options is not None:
            loader.set_user_options_from_yml(user_options)
    else:
        loader.initialise_with_default()

    if url:
        typer.echo(f"Accessing block {url}")
        version_id, pathspec = None, None
        try:
            version_id = decode_oxa_link(url)
        except ValueError:
            pathspec = decode_url(url)
            typer.echo("Decoded {pathspec}")

        try:
            block = session.get_block(
                version_id.project if version_id is not None else pathspec.project,
                version_id.block if version_id is not None else pathspec.block,
            )
            typer.echo(f"Found & retreived block: {block.name}")
        except ValueError as err:
            typer.echo(err)
            typer.echo("Could not find block or you do not have access")
            raise typer.Exit(code=1) from err

        try:
            LatexProjectBuilder.build_single_article_by_url(loader, session, url)
        except ValueError as err:
            typer.echo(err)
            raise typer.Exit(code=1)

        typer.echo("Exiting...")
        return typer.Exit(code=0)

    try:
        project_obj = session.get_project(project)
        typer.echo(f"Found project: {project_obj.name}")
    except ValueError as err:
        typer.echo(f"Could not find project: {project} or you do not have access")
        raise typer.Exit(code=1) from err

    try:
        LatexProjectBuilder.build_single_article_by_name(
            loader, session, project_obj, article, version
        )
    except ValueError as err:
        typer.echo(err)
        raise typer.Exit(code=1)

    typer.Exit(code=0)
