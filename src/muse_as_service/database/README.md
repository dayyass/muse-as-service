### Database
Since the service is usually running on the server, it is important to restrict access to the service.

For this reason, MUSE as Service uses **token-based authorization** with [JWT](https://jwt.io) for users in sqlite database [app.db](https://github.com/dayyass/muse_as_service/tree/main/muse_as_service/database/app.db).

Initially database has only one user with:
- **username**: "admin"
- **password**: "admin"

To add new user with `username` and `password` run:
```
python src.muse_as_service/database/add_user.py --username {username} --password {password}
```
**NOTE**: run it from parent directory `muse_as_service`

**NOTE**: no passwords are stored in the database, only their hashes.

To remove the user with `username` run:
```
python src.muse_as_service/database/remove_user.py --username {username}
```
**NOTE**: run it from parent directory `muse_as_service`
