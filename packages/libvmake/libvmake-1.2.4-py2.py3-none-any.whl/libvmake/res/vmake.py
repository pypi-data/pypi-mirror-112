# /usr/bin/env python3

# encoding: utf-8
import os
import sys
import argparse
import logging
from libvmake import libvmake
from libvmake import utils as libvmake_utils
import yaml

libvmake.enable_debug()

logging.basicConfig(
    level=logging.DEBUG, format="%(time)s:%(level)s %(message)s")

log = logging.getLogger('vmake')

# check suitable platform
if sys.platform not in ['win32']:
    libvmake.abort("system platform is not supported")

# check if running with root privilege
# checkroot()

# with open(libvmake.current_file('config.yml'), mode='r', encoding='utf-8') as f:
#     config = yaml.load(f.read(), Loader=yaml.FullLoader)['config']

parsed_args = None
parser = None

# os.environ['bash'] = libvmake.get_bash()

# libvmake_utils.set_proxy_from_config()
# log.info(f"set proxy to {os.environ['HTTP_PROXY']} {os.environ['HTTPS_PROXY']}")

@libvmake.task(help="this is a test task")
def test():
    log.info("abc")


@libvmake.task(help="show help document")
def help():
    if parser is not None:
        parser.print_help()


def _parse_arg(parser: argparse.ArgumentParser):
    parser.add_argument('--foo', action="store", required=False,
                        help="specify the foo option value")
    parser.add_argument('--debug', action="store_true", required=False,
                        help="debug the task script")

parsed_args, parser = libvmake.parse_args(_parse_arg)

# run task
libvmake.run_task()
