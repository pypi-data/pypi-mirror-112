import re
import logging
from .SchemaOptionDefs import SchemaOptionDefs
from .BooleanSchemaOption import BooleanSchemaOption


def citep_transform(content: str):
    logging.info("Transform: citep_transform")
    return re.sub(r"\\citep{", r"\\cite{", content)

class CitepSchemaOption(BooleanSchemaOption):
    def __init__(self):
        super(CitepSchemaOption, self).__init__()

        self.add(True, SchemaOptionDefs(
            packages=["package-natbib.def"],
            setup=["setup-bib-style.def", "setup-cite-style.def"]
            )
        )

        self.add(False, SchemaOptionDefs(
            transforms=[citep_transform]
        ))

        self.set_default(True)
