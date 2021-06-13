from muse_as_service import create_app, download_thhub_model

app = create_app()


if __name__ == "__main__":
    download_thhub_model()
    app.run(host="0.0.0.0", port=5000)
