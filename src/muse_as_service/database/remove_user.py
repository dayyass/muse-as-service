import sqlite3
from argparse import ArgumentParser
from contextlib import closing


def get_argparse() -> ArgumentParser:
    """
    Helper function to get ArgumentParser.
    """

    parser = ArgumentParser()

    parser.add_argument(
        "--username", type=str, required=True, help="This field cannot be blank"
    )

    return parser


if __name__ == "__main__":

    # argparse
    parser = get_argparse()
    args = parser.parse_args()

    delete_query = f"DELETE FROM users WHERE username = '{args.username}';"

    # sqlite
    with closing(sqlite3.connect("muse_as_service/database/app.db")) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(delete_query)
            conn.commit()

    print(f"User '{args.username}' was deleted.")
