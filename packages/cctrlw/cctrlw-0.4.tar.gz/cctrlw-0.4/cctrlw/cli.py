#!/usr/bin/env python3
from argparse import (
    ArgumentDefaultsHelpFormatter,
    ArgumentParser,
    FileType,
    HelpFormatter,
)
from json import load
from os.path import basename
from pathlib import Path
from re import compile
from sys import argv, executable, stdin, stdout
from . import CONFIG_DIR, MODES_JSON
from .algo import dsu, get_streak, load_partitions

class CustomFormatter(ArgumentDefaultsHelpFormatter):
    def _fill_text(self, text, width, indent):
        return "".join(indent + line for line in text.splitlines(keepends=True))


__desc__ = r"""pipe "{cursor_pos} {partition} {data*}" into stdin; stdout will contain the length of longest suffix of data[:cursor_pos] with the same character type as defined by {partition}.

'--format' determines how data is treated; suppose B is raw bytes read from stdin, R is the parsed value, then:
  * for `bytes` format, R = B
   (for instance, string b'abacaba' will be treated as b'abacaba');
  * for `spacesepints`, R = bytes(int(x) for x in B.decode('utf-8').split(' '))
   (for instance, string b'0 1 2 3' will be treated as b'\x00\x01\x02\x03');"""
__cli__ = f"{executable} -m {__package__}.{basename(__file__)[:-3]}"


def parse_arguments():
    parser = ArgumentParser(
        __cli__,
        formatter_class=CustomFormatter,
        description=__desc__,
    )
    DEFAULT_CONFIG = Path(__file__).parents[1] / CONFIG_DIR / MODES_JSON
    parser.add_argument(
        "config_file",
        help="Path to a config json file.",
        nargs="?",
        const=DEFAULT_CONFIG,
        default=str(DEFAULT_CONFIG),
        type=FileType("r"),
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=["spacesepints", "bytes"],
        default="spacesepints",
        nargs="?",
        const="spacesepints",
        help="data format to be used; see description for details",
    )
    parser.add_argument(
        "-d",
        "--dump-partitions",
        action="store_true",
        default=False,
        help="dump partitions defined by config to stderr",
    )
    args = parser.parse_args()
    if isinstance(args.config_file, str):
        args.config_file = open(args.config_file, "r")
    return args


def run():
    args = parse_arguments()
    cfg = load_partitions(load(args.config_file))
    if args.dump_partitions:
        for name, part in cfg.items():
            print(f"{name}: {part}")
    else:
        R = compile(b"^(?P<cursor>[0-9]+) (?P<partition>[^ ;]+) (?P<data>.*)$")
        data = stdin.buffer.read()
        S = R.match(data)
        assert S, f"match failed; input was '{data}'"
        cursor, partition, data = map(bytes, S.groups())
        cursor, partition = (x.decode("utf-8") for x in (cursor, partition))
        cursor, partition = int(cursor), cfg.get(partition)
        data = (data[:cursor])[::-1]
        print(get_streak(data, partition), end="")


if __name__ == "__main__":
    run()
else:
    raise RuntimeError("this module is supposed to be run, not imported")
