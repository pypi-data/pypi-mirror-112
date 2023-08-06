import argparse
import json
from pathlib import Path
from typing import Any, List

import toml
import yaml

from .const import (CODE_EXAMPLE, CONFIG_IGNORE, ENV, ENV_ONLY_EXAMPLE,
                    FORMATS, GITIGNORE, SECRETS, SETTINGS, PathDescriptor,
                    Singleton, open_file)


class Parser:
    switcher = {
        "JSON": lambda string: json.load(string),
        "TOML": lambda string: toml.load(string),
        "YAML": lambda string: yaml.load(string),
        "YML": lambda string: yaml.load(string),
    }

    @staticmethod
    def parser(obj: "MyConfig", filenames: List[Path]):
        for file in filenames:
            f = open_file(file)
            _format = str(file).split(".")[-1]
            try:
                data = Parser.switcher[_format.upper()](f)
                for key in data.keys():
                    obj.__setattr__(key.replace("-", "_"), data[key])
                f.close()
            except KeyError:
                raise Exception("File format error")

    @staticmethod
    def env_parse(value: Any):
        if value.isdigit():
            return int(value)
        elif value.lower() in ["true", "false"]:
            if value.lower() == "true":
                return True
            return False
        elif value.startswith("[") and value.endswith("]"):
            value = [x.strip() for x in value[1:-1].split(",")]
            return [Parser.env_parse(var) for var in value]
        elif value == "":
            return None
        return value


class MyConfig(metaclass=Singleton):
    _filenames = PathDescriptor("_filenames")

    def __init__(self, filenames: List[str] = None) -> None:
        if filenames:
            self._filenames = filenames
            Parser.parser(self, self._filenames)
        if ENV.exists():
            file = open_file(ENV)
            for line in file:
                key, value = line.strip("\n").split("=", 1)
                value = Parser.env_parse(value)
                self.__setattr__(key, value)

    def __getattr__(self, key: str) -> Any:
        return self.__dict__.get(key, None)

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "_filenames":
            return super().__setattr__(name, value)
        return self.__dict__.update({name: value})


def init(_format: str) -> None:
    file = open(str(Path("settings.py")), "w", encoding="utf-8")
    if _format:
        if _format not in FORMATS:
            raise Exception("Unknown format.")
        for _file in [SETTINGS, SECRETS]:
            open(str(Path("%s.%s" % (_file, _format))), "a", encoding="utf-8").close()
            print("Created: %s.%s" % (_file, _format))
        file.write(
            CODE_EXAMPLE.format(
                "%s.%s" % (SETTINGS, _format),
                "%s.%s" % (SECRETS, _format),
            )
        )
        file.close()
        if GITIGNORE.exists():
            with open(str(GITIGNORE), "r+", encoding="utf-8") as gitignore_file:
                text = gitignore_file.read() + CONFIG_IGNORE.format(SECRETS + ".*")
                gitignore_file.seek(0)
                gitignore_file.write(text)
    else:
        file.write(ENV_ONLY_EXAMPLE)
        file.close()
    print("Created: settings.py")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--init", default=None, type=str, nargs="?")
    args = parser.parse_args()
    return init(args.init)


if __name__ == "__main__":
    main()
