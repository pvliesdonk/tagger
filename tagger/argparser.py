import argparse
import logging
import sys
from pathlib import Path


class Argparser:

    def __init__(self, cmd_line=None):
        self.logger = logging.getLogger(__name__)
        self.argparser = self.define_arg_parser()
        self.args_parsed = self.parse(cmd_line)

        self.files = None
        self.indirs = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

    @staticmethod
    def define_arg_parser():
        arg_parser = argparse.ArgumentParser(prog=sys.argv[0],
                                             description="Tag MP3 files.",
                                             add_help=True,
                                             allow_abbrev=False)

        # define logging verbosity
        arg_parser.add_argument(
            '--verbose', '-v', action='count', default=0
        )

        arg_parser.add_argument(
            "files", metavar="<FILENAME>", nargs='*',
            help="Filenames for file that must be processed"
        )

        arg_parser.add_argument(
            "-i", "--indir", dest='indirs', metavar="<IN_DIR>", action='append',
            help="One or more directories that get recursively processed", default=None
        )

        arg_parser.add_argument(
            "-d", "--dry-run", dest='dryrun', action='store_true', default=False
        )

        return arg_parser

    def parse(self, cmd_line=None):
        if cmd_line is None:
            self.args_parsed = self.argparser.parse_args()
        else:
            self.logger.debug("")
            self.args_parsed = self.argparser.parse_args(cmd_line)

        return self.args_parsed

    def get_args(self):
        return self.args_parsed

    def get_verbosity(self):
        if self.args_parsed.verbose > 2:
            return logging.DEBUG
        if self.args_parsed.verbose > 1:
            return logging.INFO
        if self.args_parsed.verbose > 0:
            return logging.WARNING
        return logging.ERROR

    def is_dryrun(self):
        return self.args_parsed.dryrun

    def get_files(self):
        if self.files is None:
            self.files = []
            for f in self.args_parsed.files:
                p = Path(f)
                if p.exists():
                    self.files.append(p)
                else:
                    self.logger.error(f"File {f} does not exist")
        return self.files


    def get_indirs(self):
        if self.indirs is None and self.args_parsed.indirs is not None:
            self.indirs = []
            for d in self.args_parsed.indirs:
                p = Path(d)
                if p.exists():
                    self.indirs.append(p)
                else:
                    self.logger.error(f"Directory {d} does not exists.")
        return self.indirs

    def get_all_files(self):
        # get all files from cmdline
        for p in self.get_files():
            yield p

        # also get all files from all directories
        for p in  self.get_indirs():
            for f in p.glob('**/*.mp3'):
                yield f
