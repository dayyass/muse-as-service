from muse_as_service import create_app, get_argparse, download_thhub_model

app = create_app()


if __name__ == "__main__":

    # argparse
    parser = get_argparse()
    args = parser.parse_args()

    # run
    download_thhub_model()
    app.run(host=args.host, port=args.port)
