---
Title: PHP
...

# PHP

**WARNING**: Using PHP for Director sites is discouraged. We strongly recommend that you use a more modern framework like [Django](django.md).

To use PHP on Director, set the site type to `Dynamic` and choose the `PHP` image. You will need to use the default `run.sh` template, or at least something based off of it.

### Accessing files

If you try to write to files (or read from certain files) on a PHP site, you may encounter permission errors. This is caused by technical limitations. [^1]

Adding these two lines to your `run.sh` (after the `#!/bin/sh` shebang, but before the `exec apache2-foreground` line) should fix things:

```sh
umask 002
sh -c 'while true; do chmod -R g=u /site; sleep 5; done' &
```

(Yes, this is extremely hacky. There isn't really a better option.)

[^1]: <small>Your code runs as `root` inside the Docker container. However, Apache, the web server used to serve PHP sites, has a hardcoded requirement that it *not* run as `root`. As a result, this workaround is necessary.</small>
