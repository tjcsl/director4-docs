---
Title: Don't hardcode your site's database URL
...

# Don't hardcode your site's database URL

If your site has a database created, and you pull up the page with all your site's information, you will notice that the URL for accessing your site's database is shown right there. You may be tempted to simply copy/paste it into your site's configuration (or, if you need the individual components separately, to copy/paste them one by one). **Do not do this.**

**Your site's database URL can change at any time without warning.** If you click the `Regenerate site secrets` button, the database password is regenerated. Additionally, if Director undergoes internal changes, other parts of the database URL may change.

### Always use the `DIRECTOR_DATABASE_URL` [^1] environmental variable to connect to a database.

This is in the format `database_type://username:password@host:port/database_name`.

#### *But what if my database client requires the different parts of the URL (username, password, etc.) separately?*

Director also exports the following environmental variables containing individual pieces of connection information:

- `DIRECTOR_DATABASE_TYPE`: The database type (`postgres`/`mysql`)
- `DIRECTOR_DATABASE_HOST`: The hostname of the database server
- `DIRECTOR_DATABASE_PORT`: The port on the database server to connect to
- `DIRECTOR_DATABASE_NAME`: The name of this site's database
- `DIRECTOR_DATABASE_USERNAME`: The name of the user to connect to the database as
- `DIRECTOR_DATABASE_PASSWORD`: The user's password

You can use these parameters instead.

### For examples of how to connect to your database in various languages, see the [MySQL](mysql.md) and [PostgreSQL](postgresql.md) pages.

[^1]: <small>A previous version of Director exported the database URL through the `DATABASE_URL` environmental variable. This is also supported for backwards compatibility.</small>
