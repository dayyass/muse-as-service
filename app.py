from muse_as_service.app import app
from muse_as_service.utils import get_argparse, get_logger

if __name__ == "__main__":

    # argparse
    parser = get_argparse()
    args = parser.parse_args()

    # logger
    logger = get_logger()

    # run
    app.run(host=args.host, port=args.port)
