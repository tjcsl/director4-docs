# Minimalism

Director is not designed to run intensive tasks, especially those that require a lot of CPU or RAM usage.

For instance:

* Do not use a file to store data and read them on every startup. Instead, use a database (PostgreSQL or MySQL).
* Keep Docker images small. Don't install unnecessary software - for instance, `bash` and `tmux` are often unnecessary.
* Use Alpine images when possible. They are smaller than Debian images, which will result in faster performance.
