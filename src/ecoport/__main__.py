import argparse
import json
import subprocess
from copy import deepcopy
from typing import List

import yaml

PKG_KEY = "dependencies"


class Config:
    _all_configs = ["exclusions"]
    _default_configs = {"exclusions": []}

    def __init__(self, args: argparse.Namespace):
        if args.config is not None:
            with open(args.config, "r") as f:
                config = yaml.safe_load(f)
            config = {k: v for k, v in config.items() if k in self._all_configs}
        else:
            config = deepcopy(self._default_configs)

        if args.exclusions is not None:
            config["exclusions"] = args.exclusions

        self._config = config

    def apply(self, env) -> dict:
        env[PKG_KEY] = [
            pkg
            for pkg in env[PKG_KEY]
            if isinstance(pkg, str) and pkg.split("=")[0] not in self._config["exclusions"]
        ]
        return env


def get_history_export_pkg_names() -> List[str]:
    history_env = yaml.safe_load(
        subprocess.check_output("conda env export --from-history".split(" "))
    )
    return [pkg.split("=")[0] for pkg in history_env[PKG_KEY]]


def filt_conda_pkg_by_name(names: List[str], env: dict) -> dict:
    res = deepcopy(env)
    res[PKG_KEY] = []
    for pkg in env[PKG_KEY]:
        # pip
        if isinstance(pkg, dict):
            continue
        name, ver, _ = pkg.split("=")
        if name in names:
            res[PKG_KEY].append(f"{name}={ver}")
    return res


def main(args: argparse.Namespace):
    pkg_names = [n for n in get_history_export_pkg_names()]

    full_env = yaml.safe_load(subprocess.check_output("conda env export".split(" ")))

    full_env = filt_conda_pkg_by_name(pkg_names, full_env)

    if args.no_prefix:
        del full_env["prefix"]

    config = Config(args)
    full_env = config.apply(full_env)

    with open(args.filename, "w") as f:
        yaml.safe_dump(full_env, f, sort_keys=False, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, default="environment.yaml", dest="filename")
    parser.add_argument("--no-prefix", action="store_true", dest="no_prefix")
    parser.add_argument("--exclusions", type=str, nargs="+")
    parser.add_argument("--config", type=str)
    args = parser.parse_args()

    main(args)
