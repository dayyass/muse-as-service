from muse_embedder import create_app, download_thhub_model

app = create_app()


if __name__ == "__main__":
    download_thhub_model()
    app.run()
