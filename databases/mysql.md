---
Title: MySQL Databases
...

# MySQL Databases

This page assumes you've read the [Quick Start guide](quick-start.md) and created a MySQL database for your site.

[TOC]

## Managing your site's database

For an interactive shell where you can type SQL queries and see responses, click `Database shell` under the `Database` section on your site's information page.

To delete your database, click `Delete Database`. **WARNING**: This will irrevocably delete ALL data stored in your site's database.

## How to access your database from your site's server

Here are some examples of how to access Director MySQL databases in different languages.

*Note: All of these examples assume you have installed the necessary libraries and set everything else up. This page is a guide for getting Director databases to work with different frameworks; **it is not a general "how to do web development in X" guide**.*

Additionally, please read the relevant [Framework Guides](../framework-guides).

### Node

Using the [`mysql`](https://github.com/mysqljs/mysql) library:

```javascript
var mysql = require('mysql');
var connection = mysql.createConnection(process.env.DIRECTOR_DATABASE_URL);
```

### Django

Adding this to your `settings.py` should work:

```python
import os

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ["DIRECTOR_DATABASE_NAME"],
        "USER": os.environ["DIRECTOR_DATABASE_USERNAME"],
        "PASSWORD": os.environ["DIRECTOR_DATABASE_PASSWORD"],
        "HOST": os.environ["DIRECTOR_DATABASE_HOST"],
        "PORT": os.environ["DIRECTOR_DATABASE_PORT"],
    },
}
```

Alternatively, if you have your code in Git (see [Version Control Best Practices](../best-practicies/version-control.md)) and you want it to work without modification on your computer, this will let you fall back on an SQLite database when not on Director:

```python
import os

if "DIRECTOR_DATABASE_URL" in os.environ:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.environ["DIRECTOR_DATABASE_NAME"],
            "USER": os.environ["DIRECTOR_DATABASE_USERNAME"],
            "PASSWORD": os.environ["DIRECTOR_DATABASE_PASSWORD"],
            "HOST": os.environ["DIRECTOR_DATABASE_HOST"],
            "PORT": os.environ["DIRECTOR_DATABASE_PORT"],
        },
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }
```

### SQLAlchemy (for example, with Flask)

```python
import os
from sqlalchemy import create_engine

engine = create_engine(os.environ["DIRECTOR_DATABASE_URL"])
```

If you want to use an SQLite database when your code is not run on Director, like the Django example above:

```python
import os
from sqlalchemy import create_engine

engine = create_engine(os.environ.get("DIRECTOR_DATABASE_URL", "sqlite:///<path to local database file>"))
```

And if you need to specify an alternate *driver* (see the [SQLAlchemy docs](https://docs.sqlalchemy.org) for details), you can use this:

```python
import os
from sqlalchemy import create_engine

if "DIRECTOR_DATABASE_URL" in os.environ:
    db_url = os.environ["DIRECTOR_DATABASE_URL"]
    driver_name = "<name of the driver you want to use>"
    db_colon_index = db_url.index(":")
    db_url = db_url[:db_colon_index] + "+" + driver_name + db_url[db_colon_index:]
else:
    db_url = "sqlite:///<path to local database file>"

engine = create_engine(db_url)
```

### PHP

**WARNING**: Usage of PHP on Director is not recommended.

Using PDO:

```php
$db = new PDO("mysql:dbname=" . getenv("DIRECTOR_DATABASE_NAME") . ";host=" . getenv("DIRECTOR_DATABASE_HOST") . ";port=" . getenv("DIRECTOR_DATABASE_PORT"), getenv("DIRECTOR_DATABASE_USERNAME"), getenv("DIRECTOR_DATABASE_PASSWORD"));
```

Using the `mysqli_*()` functions:

```php
$db = mysqli_connect(getenv("DIRECTOR_DATABASE_HOST"), getenv("DIRECTOR_DATABASE_USERNAME"), getenv("DIRECTOR_DATABASE_PASSWORD"), getenv("DIRECTOR_DATABASE_NAME"), getenv("DIRECTOR_DATABASE_PORT"));
// OR
$db = new mysqli(getenv("DIRECTOR_DATABASE_HOST"), getenv("DIRECTOR_DATABASE_USERNAME"), getenv("DIRECTOR_DATABASE_PASSWORD"), getenv("DIRECTOR_DATABASE_NAME"), getenv("DIRECTOR_DATABASE_PORT"));
```
