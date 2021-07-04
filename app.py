from muse_as_service.flask_app import create_app
from muse_as_service.utils import download_thhub_model, get_argparse

app = create_app()


if __name__ == "__main__":

    # argparse
    parser = get_argparse()
    args = parser.parse_args()

    # load model
    download_thhub_model()

    # run
    print(f" * Token: {app.token}")

    app.run(host=args.host, port=args.port)
