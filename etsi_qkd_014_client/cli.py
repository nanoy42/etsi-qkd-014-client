# Copyright (C) 2022 Yoann Piétri
# Copyright (C) 2022 LIP6 - Sorbonne Université
#
# etsi-qkd-14-client is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# etsi-qkd-14-client is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with etsi-qkd-14-client. If not, see <http://www.gnu.org/licenses/>.

"""
Command line interface commands to test the module.
"""

import argparse
import configparser
import logging
from typing import Tuple

from etsi_qkd_014_client import __version__
from etsi_qkd_014_client.client import QKD014Client

logger = logging.getLogger(__name__)


def main() -> None:
    """
    Entrypoint of the command line tool.
    """
    parser = argparse.ArgumentParser(prog="qkd014-client")
    parser.add_argument("--version", action="version", version=__version__)

    subparsers = parser.add_subparsers()

    get_status_parser = subparsers.add_parser(
        "get_status", help="Get status of the SAE"
    )
    get_status_parser.set_defaults(func=get_status)

    get_key_parser = subparsers.add_parser("get_key", help="Get a key from SAE")
    get_key_parser.set_defaults(func=get_key)

    get_key_with_id_parser = subparsers.add_parser(
        "get_key_with_id", help="Get a key from SAE with specific ID"
    )
    get_key_with_id_parser.add_argument(
        "key_id", help="KEY ID when asking for a specific key."
    )
    get_key_with_id_parser.set_defaults(func=get_key_with_id)

    parser.add_argument(
        "sae_id", help="ID of the SAE (slave or master depending on the command)"
    )
    parser.add_argument("-H", "--hostname", help="Hostname of the KME.")
    parser.add_argument("-c", "--cert", help="Path of the certificate file.")
    parser.add_argument("-k", "--key", help="Path of the key file.")
    parser.add_argument("-r", "--ca", help="Path of the root CA file.")
    parser.add_argument(
        "-f", "--force", action="store_true", help="Force insecure protocol ?"
    )
    parser.add_argument("-C", "--config", help="Give path of the configuration file.")
    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        print("No command specified. Run with -h|--help to see the possible commands.")


def read_args(args: argparse.Namespace) -> Tuple[str, str, str, str, bool]:
    """Read the args passed to the command line.

    It will first try to read the configuration file it a path was passed to the command line args.
    Otherwise it will read the parameter from the command line args.

    An exeception will be raised if any paramater is missing.

    Args:
        args (argparse.Namespace): args passed to the command line.

    Raises:
        Exception: Missing section in the configuration file.
        Exception: Missing parameter in the configuration file.
        Exception: Missing parameter in the command line args.

    Returns:
        Tuple[str, str, str, str, bool]: hostname, cert, key, ca, force
    """
    if args.config is not None:
        logger.info("Attempting to read configuration file.")

        config = configparser.ConfigParser()
        config.read(args.config)

        if "etsi_qkd_014_client" not in config.sections():
            raise Exception(
                "Configuration file does not appear to have etsi_qkd_014_client section."
            )

        if "hostname" not in config["etsi_qkd_014_client"]:
            raise Exception(
                "The etsi_qkd_014_client section does not have the hostname parameter."
            )

        if "cert" not in config["etsi_qkd_014_client"]:
            raise Exception(
                "The etsi_qkd_014_client section does not have the cert parameter."
            )

        if "key" not in config["etsi_qkd_014_client"]:
            raise Exception(
                "The etsi_qkd_014_client section does not have the key parameter."
            )

        if "ca" not in config["etsi_qkd_014_client"]:
            raise Exception(
                "The etsi_qkd_014_client section does not have the ca parameter."
            )

        if "force" not in config["etsi_qkd_014_client"]:
            raise Exception(
                "The etsi_qkd_014_client section does not have the force parameter."
            )

        hostname = config["etsi_qkd_014_client"]["hostname"]
        cert = config["etsi_qkd_014_client"]["cert"]
        key = config["etsi_qkd_014_client"]["key"]
        root_ca = config["etsi_qkd_014_client"]["ca"]
        force = config["etsi_qkd_014_client"].getboolean("force")

        logger.info("Configuration file successfully read.")
    else:
        logger.info("Attempting to read configuration from the command line arguments.")
        if args.hostname is None:
            raise Exception(
                "hostname parameter is missing. Give the hostname with -H or --hostname."
            )

        if args.cert is None:
            raise Exception(
                "cert parameter is missing. Give the cert parameter with -c or --cert."
            )

        if args.key is None:
            raise Exception(
                "key parameter is missing. Give the key parameter with -k or --key."
            )

        if args.ca is None:
            raise Exception(
                "ca parameter is missing. Give the ca parameter with -r or --ca."
            )

        if args.force is None:
            raise Exception(
                "force parameter is missing. Give the force parameter withy -f or --force."
            )
        hostname, cert, key, root_ca, force = (
            args.hostname,
            args.cert,
            args.key,
            args.ca,
            args.force,
        )
        logger.info("Command line parameters successfully read.")
    return hostname, cert, key, root_ca, force


def get_status(args: argparse.Namespace) -> None:
    """Get status command.

    Args:
        args (argparse.Namespace): args passed to the command line.
    """
    hostname, cert, key, root_ca, force = read_args(args)

    sae_id = args.sae_id

    client = QKD014Client(hostname, cert, key, root_ca, force_insecure=force)
    code, response = client.get_status(sae_id)

    print(f"Response code : {code}\n")
    print(response)


def get_key(args: argparse.Namespace) -> None:
    """Get key command.

    Args:
        args (argparse.Namespace): args passed to the command line.
    """
    hostname, cert, key, root_ca, force = read_args(args)

    sae_id = args.sae_id

    client = QKD014Client(hostname, cert, key, root_ca, force_insecure=force)
    code, response = client.get_key(sae_id)

    print(f"Response code : {code}\n")
    print(response)


def get_key_with_id(args: argparse.Namespace) -> None:
    """Get key with ID command.

    Args:
        args (argparse.Namespace): args passed to the command line.
    """
    hostname, cert, key, root_ca, force = read_args(args)

    sae_id = args.sae_id
    key_id = args.key_id

    client = QKD014Client(hostname, cert, key, root_ca, force_insecure=force)
    code, response = client.get_key_with_key_IDs(sae_id, [key_id])

    print(f"Response code : {code}\n")
    print(response)


if __name__ == "__main__":
    main()
