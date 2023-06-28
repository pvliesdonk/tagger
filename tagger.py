#!env python3

import logging
from tagger import Argparser

if __name__ == "__main__":
    # use argument parser
    with Argparser() as a:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M',
                            filename='orly_debug.log',
                            filemode='a')

        # define a Handler which writes INFO messages or higher to the sys.stderr
        console = logging.StreamHandler()
        console.setLevel(a.get_verbosity())

        # set a format which is simpler for console use
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        # tell the handler to use this format
        console.setFormatter(formatter)

        # add the handler to the root logger
        logging.getLogger('').addHandler(console)

        # create logger for main tread
        logger = logging.getLogger('Main')

        if a.is_dryrun():
            logger.info("Performing a dry run.")

        for f in a.get_all_files():
            print(f)