from typing import List, Optional


class SchemaOptionDefs:
    _passopts: List[str]
    _packages: List[str]
    _setup: List[str]

    def __init__(
        self,
        passopts: Optional[List[str]] = None,
        packages: Optional[List[str]] = None,
        setup: Optional[List[str]] = None,
    ):
        self._passopts = passopts
        self._packages = packages
        self._setup = setup

    @property
    def passopts(self):
        return self._passopts if self._passopts is not None else []

    @property
    def packages(self):
        return self._packages if self._packages is not None else []

    @property
    def setup(self):
        return self._setup if self._setup is not None else []

    @property
    def in_template(self):
        return False


class CustomTemplateDefs(SchemaOptionDefs):
    def __init__(self, *args, **kwargs):
        super(CustomTemplateDefs, self).__init__(*args, **kwargs)

    @property
    def in_template(self):
        return True
