#!/usr/bin/env python3
import gogdl.args as args
from gogdl.dl import manager
import gogdl.api as api
import gogdl.imports as imports
import logging

logging.basicConfig(
    format='[%(name)s] %(levelname)s: %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('MAIN')

def main():
    arguments = args.init_parser()
    logger.debug(arguments)
    api_handler = api.ApiHandler(arguments.token)
    download_manager = manager.DownloadManager(api_handler)

    switcher = {
        "download": download_manager.download,
        "import": imports.get_info,
        "info": download_manager.calculate_download_size
    }

    function = switcher.get(arguments.command)
    if function:
        function(arguments)

if __name__ == "__main__":
    main()