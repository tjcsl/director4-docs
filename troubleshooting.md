---
Title: Troubleshooting
...

# Troubleshooting

### Q: I created a `run.sh` file, and my site says it's running, but I get an error when I try to open the page.

A: After creating or updating your `run.sh`, you must restart your site's process for the changes to take effect. Click "Restart Process" on the site information page.

### Q: One of my site's processes keeps running out of memory and crashing. What's going on?

A: To prevent abuse, by default Director sites are allocated very limited resources. The default memory limitation for each site is 100 MB. Please try to limit your site's memory usage to stay below this.

If that is not an option and you think you have a valid reason for increased memory allocations, please contact <director@tjhsst.edu> with an explanation of why.

**Before you email: You should NOT be training neural networks or performing computationally intensive tasks on Director sites. The Syslab has two high-performance clusters and two workstations with high-end GPUs specifically for this purpose.**

### Q: My site works, but it runs very slowly.

A: Just like the memory limit, each site's CPU usage is also limited. If you absolutely need your site to be allowed more CPU usage and you think you have a valid reason, please see the contact instructions above.

### Q: My site suddenly can't access its database anymore.

You likely hardcoded your site's database URL into your application. Please see [Don't hardcode your site's database URL](databases/no-hardcode-url.md).

Note: If you regenerated your database password, any terminals you have open will not (and cannot) be automatically updated. Try reloading the page to launch a new terminal.

### Q: My site's server starts, and everything's running, but I get a `502 Bad Gateway` error when I try to open it.

You need to set up your site's server to listen on the port specified by the `PORT` environmental variable, but also to bind to the address specified by the `HOST` environmental variable. This is a change from previous versions of Director.

Some servers will want you to specify these two together in the format `host:port`, and call this the "bind address," "listen address." or something similar. Others will have them as separate options, and refer to the host as "bind address," "listen address," "host," or something similar. It varies.
