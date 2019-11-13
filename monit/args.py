"""Deals with arguments given to the script

To start with the only arguments will require one argument
"""

import argparse
import sys


def parse_args():
    """Generate argument parsers

    Returns:
    argparse object
    """
    args = sys.argv[1:]

    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers()

    parser.add_argument(
        "--version",
        action="store_true",
        default=False,
        dest='version',
        help="Print currently installed version")

    # add arguments for sub-parsers
    add_resources_subparser(subparser)
    add_jobs_subparser(subparser)

    return parser.parse_args(args)


def add_jobs_subparser(subparser):
    """Add optional arguments for the 'reports' sub-command.
    Arguments:
    subparser -- Object form argparse.ArgumentParser().add_subparsers()
    """
    # Initiate parser.
    parser = subparser.add_parser(
        'jobs',
        help="Gather information about resources pool.")
    subparser = parser.add_subparsers()

    # Set the sub-command routine to run.
    parser.set_defaults(cmd='jobs')


def add_resources_subparser(subparser):
    """Add optional arguments for the 'reports' sub-command.
    Arguments:
    subparser -- Object form argparse.ArgumentParser().add_subparsers()
    """
    # Initiate parser.
    parser = subparser.add_parser(
        'resources',
        help="Gather information about resources pool.")
    subparser = parser.add_subparsers()

    # Set the sub-command routine to run.
    parser.set_defaults(cmd='resources')

