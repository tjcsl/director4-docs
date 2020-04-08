---
Title: Troubleshooting
...

# Troubleshooting

[TOC]

### I created a `run.sh` file, and my site says it's running, but I get an error when I try to open the page.

After creating or updating your `run.sh`, you must restart your site's process for the changes to take effect. Click `Restart Process` on the site information page.

### I created a `run.sh` file, and my site says it's running, but I get an error when I try to open the page.

Depending on the framework you use, you may need to restart your site's process when you edit your site's files.

### One of my site's processes keeps running out of memory and crashing. What's going on?

To prevent abuse, by default Director sites are allocated very limited resources. The default memory limitation for each site is 100 MB. Please try to limit your site's memory usage to stay below this.

If that is not an option and you think you have a valid reason for increased memory allocations, please contact <director@tjhsst.edu> with an explanation of why.

**Before you email: You should NOT be training neural networks or performing computationally intensive tasks on Director sites. The Syslab has two high-performance clusters and two workstations with high-end GPUs specifically for this purpose.**

### My site works, but it runs very slowly.

Just like the memory limit, each site's CPU usage is also limited. If you absolutely need your site to be allowed more CPU usage and you think you have a valid reason, please see the contact instructions above.

### My site suddenly can't access its database anymore.

You likely hardcoded your site's database URL into your application. Please see [Don't hardcode your site's database URL](databases/no-hardcode-url.md).

Note: If you regenerated your database password, any terminals you have open will not (and cannot) be automatically updated. Try reloading the page to launch a new terminal.

### My site's server starts, and everything's running, but I get a `502 Bad Gateway` error when I try to open it.

You need to set up your site's server to listen on the port specified by the `PORT` environmental variable, but also to bind to the address specified by the `HOST` environmental variable. This is a change from previous versions of Director.

Some servers will want you to specify these two together in the format `host:port`, and call this the "bind address," "listen address." or something similar. Others will have them as separate options, and refer to the host as "bind address," "listen address," "host," or something similar. It varies.

### My site's process never starts and/or I get an error every time I try to open a terminal.

Did you delete the `.home` directory in your site's main directory? The `.home` directory is automatically created, but it is not recreated if you delete it, and it must exist for your site to work properly.

This may also occur if you use a large Debian-based Docker image. Debian images are large and very slow, and sometimes they take so long to perform basic operations that the operation times out and errors. If possible, try using an Alpine-based image.

### I clicked one of the buttons/edited something on my site, but the `Ongoing operation` in the upper right just shows `Pending`.

Director can only run a limited number of operations at the same time. Yours should start eventually.

If it still has not started after an extended period of time (>1 hour), please email <director@tjhsst.edu>.

### I tried to create a custom Docker image, but it's taking forever on `Building Docker image`.

This is expected. Building Docker images takes a long time, especially if you have selected a large number of packages (or a small number of large packages) for installation.
