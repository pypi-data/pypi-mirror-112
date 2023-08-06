from sd_utils.github.fileio import get_file
from typing import Any, Dict, Set
import yaml


class GithubAction:
    """
    Metadata class about a github action
    """

    def __init__(
        self,
        owner: str,
        repo: str,
        working_environ: dict,
        token: str = "",
        required_builtins: Set[str] = {},
    ):
        self._owner = owner
        self._repo = repo
        self._working_environ = working_environ
        self._token = token
        self._required_builtins = required_builtins

        self._inputs = {}
        self._builtins = {}
        self._metadata = {}

        self.__validate_definition()
        self.__validate_environ()

    @property
    def owner(self) -> str:
        """
        The owner of the github action's source repo
        """
        return self._owner

    @property
    def repo(self) -> str:
        """
        The source repo of this github action 
        """
        return self._repo

    @property
    def inputs(self) -> Dict[str, Any]:
        """
        All the inputs defined by the action 
        file stored as a dictionary
        """
        return self._inputs

    @property
    def builtins(self) -> Dict[str, Any]:
        return self._builtins

    def __validate_definition(self):
        """
        Validates this repo as a github action
        """
        # get `action.yml` from repo
        # if not defined raise error (this will be done by the request)
        file_content = get_file(
            self._owner, self._repo, "action.yml", self._token
        )
        self._metadata = yaml.safe_load(file_content)

    def __validate_environ(self):
        """
        Validates that this action can operate
        with the given environment

        populates the `_inputs` and `_builtins` members
        """
        # validate inputs first
        for key, value in self._metadata["inputs"].items():
            environ_key = f"INPUT_{key.upper()}"
            if environ_key not in self._working_environ:
                if value["required"]:
                    raise ValueError(f"Expected input [{key}] to be defined")
                continue
            self._inputs[key] = self._working_environ[environ_key]

        # validate builins
        for builtin in self._required_builtins:
            environ_key = f"GITHUB_{builtin.upper()}"
            if environ_key not in self._working_environ:
                raise ValueError(
                    f"Expected builtin [{builtin}] to be defined. Check that this is the correct name"
                )
            self._builtins[builtin] = self._working_environ[environ_key]

        # no longer need this, just delete from memory
        del self._metadata
