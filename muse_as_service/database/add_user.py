import sqlite3
import sys
from argparse import ArgumentParser
from contextlib import closing

sys.path.append(".")
from database import UserModel  # noqa: E402


def get_argparse() -> ArgumentParser:
    """
    Helper function to get ArgumentParser.
    """

    parser = ArgumentParser()

    parser.add_argument(
        "--username", type=str, required=True, help="This field cannot be blank"
    )
    parser.add_argument(
        "--password", type=str, required=True, help="This field cannot be blank"
    )

    return parser


if __name__ == "__main__":

    # argparse
    parser = get_argparse()
    args = parser.parse_args()

    insert_query = f'INSERT INTO users (username, password) VALUES ("{args.username}", "{UserModel.generate_hash(args.password)}");'

    # sqlite
    with closing(sqlite3.connect("muse_as_service/database/app.db")) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(insert_query)
            conn.commit()

    print(f"User '{args.username}' was created.")
