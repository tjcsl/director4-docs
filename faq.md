---
Title: FAQ
...

# Frequently Asked Questions

### Who wrote Director?

Director 3.0 was originally written by primarily Eric Wang (2017) and Omkar Kulkarni (2019). The current version of Director, Director 4.0, was written by John Beutner (2020) and Theo Ouzhinski (2020) based off of Director 3.0.

### Do you have plans to add an offline mode to Director?

**Short answer:** No.

**Long answer:** An offline mode for Director would be very limited. Since your site runs on a server at TJ, you wouldn't be able to view your site, only edit files (at least for dynamic sites). Additionally, such a system would be very difficult for the Director developers to implement technically, and the slight benefit gained does not outweigh these concerns.

If you really need to work on your site offline, you may want to put your code in [Git](https://git-scm.com) and upload it to [GitHub](https://github.com) or [GitLab](https://gitlab.com).

### On my site's main page, I see a `Database Shell` link and an `Alternate shell` link. What's the difference?

`Database Shell` gives you a shell where you can type SQL queries and see the result. However, it does this by connecting directly to the server, rather than running the `mysql` or `psql` commands (which was what previous versions of Director did). As a result, you can only enter normal SQL queries -- commands like `SOURCE` in MySQL and `\dt` in PostgreSQL won't work.

`Alternate shell` runs the appropriate `mysql` or `psql` command to connect to your site's database. In this shell, commands like `SOURCE` in MySQL and `\dt` in PostgreSQL *will* work. However, for complicated technical reasons, this shell type takes much longer to load, so you may want to use `Database Shell` for quick operations.
