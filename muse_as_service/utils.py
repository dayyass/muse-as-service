from argparse import ArgumentParser


def get_argparse() -> ArgumentParser:
    """
    Helper function to get ArgumentParser.
    """

    parser = ArgumentParser()

    parser.add_argument(
        "--host",
        type=str,
        required=False,
        default="0.0.0.0",
        help="the hostname to listen on, set this to '0.0.0.0' to have the server available externally as well",
    )
    parser.add_argument(
        "--port",
        type=int,
        required=False,
        default=5000,
        help="the port of the webserver",
    )

    return parser
