import argparse
import os
import signal
import sys
import threading
import time
from typing import Callable

from logbook import Logger, StreamHandler  # type: ignore

from hansken_extraction_plugin.api.extraction_plugin import BaseExtractionPlugin
from hansken_extraction_plugin.runtime.extraction_plugin_server import serve_indefinitely
from hansken_extraction_plugin.runtime.reflection_util import get_plugin_class

log = Logger(__name__)


def hardkill():
    """
    Method that can be used to fully kill the current application. This is
    useful in cases where all other ways to stop the application fails.
    """
    time.sleep(.2)
    log.error('Failed to stop process, taking drastic measures now, goodbye cruel world!')
    try:
        os._exit(1)
    finally:
        os.kill(os.getpid(), signal.SIGKILL)


def serve(extraction_plugin_class: Callable[[], BaseExtractionPlugin], port=8999):
    log.info(f'Serving chat plugin on port {port}...')
    serve_indefinitely(extraction_plugin_class, f'[::]:{port}')

    # we are leaving the main thread, start a small thread to kill the entire
    # application if we don't exit gracefully when some other threads are
    # blocking the application to stop
    threading.Thread(target=hardkill, daemon=True).start()


def main():
    """
    Run an Extraction Plugin according to provided arguments.
    """
    log_handler = StreamHandler(sys.stdout, bubble=True, level='DEBUG')
    with log_handler.applicationbound():
        parser = argparse.ArgumentParser(prog='serve_plugin',
                                         usage='%(prog)s FILE PORT (Use -h for help)',
                                         description='Run an Extraction Plugin according to provided arguments.')

        parser.add_argument('file', metavar='FILE', help='Path of the python file of the plugin to be served.')
        parser.add_argument('port', metavar='PORT', help='Port where plugin is served on.', type=int)

        arguments = parser.parse_args()
        plugin_file = arguments.file
        port = arguments.port

        if (not plugin_file.endswith('.py')):
            log.error('Not a python file: ' + plugin_file)
            sys.exit(1)

        plugin_class = get_plugin_class(plugin_file)
        if plugin_class is not None:
            serve(plugin_class, port)
        else:
            log.error('No Extraction Plugin class found in ' + plugin_file)
            sys.exit(1)
