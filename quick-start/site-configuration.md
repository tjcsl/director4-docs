---
Title: Site Configuration
...

# Site Configuration

After creating a site, you should be shown a page with some information about that site, as well as several buttons. Here's what all those buttons do:

- `Web Terminal`: This is a link to a page that gives you an online terminal where you can interact with your site's files. Use this if you feel comfortable at a terminal.
- `Online Editor`: This is a link to the online editor, where you will likely spend the vast majority of your time working on your Director site. See [Using the Online Editor](#using-the-online-editor) below for more details.
- `Restart process`: For dynamic sites, this button restarts your site's main process. In a lot of cases, you'll need to restart your website to apply changes. (You can also restart your site's process by pressing Alt+Enter on the online editor page.)
- `Rewrite Configuration`: Director uses a server called Nginx to route traffic between sites, and this button regenerates your site's Nginx configuration. It isn't particularly useful, but it may help if your site randomly breaks for no apparent reason.
- `Regenerate secrets`: If your site has a database, this button regenerates the database password. It may also regenerate some other "secret" information. In the process, it will usually restart your site to apply the changes.
- `Customize Docker image`: This is a link to a page where you can configure your site's Docker image. See [Custom Docker Images](#custom-docker-images) below.
- `Back`: This is just a link back to the main page, with the list of all the sites.
- `Configure Site`: See [The Configure Site Page](#the-configure-site-page) below.
- `Delete Site`: This is a link to a page that asks you to confirm that you want to delete your site.
   **WARNING**: If you delete your site, there is no going back. Your files are **gone**. Make absolutely certain that you don't need anything from it.

## The Configure Site Page

The `Configure Site` page lets you edit various attributes of your site. You can rename it (except for personal sites), add custom domains (see [Custom Domains](/custom-domains.md) for details), edit the description, add other users, and change the site type.

One of the things you may notice quickly is that there are three sections separated by horizontal bars. You can only edit the data in one section at a time, and you need to click **that section's** Save button to save your changes.

The reason for this admittedly strange setup is that the settings on this page are grouped by the type of changes that need to be made internally to properly apply them. For example, renaming a site requires similar configuration changes as adding custom domains; the same is true of editing the description and adding users.

## Custom Docker Images

Director runs each site in a [Docker](https://www.docker.com/) container, and the `Customize Docker image` page lets you customize the Docker image used by your site. [^1]

#### Choosing an Image

At the top, you'll see a long list of images. You can select whichever one of these you want your site to use. (By default, your site is given a standard Alpine image, which isn't much use.)

Your choice of image will heavily depend on which web framework you use. If you're feeling a little overwhelmed by all the options, we recommend you take a look at the relevant [Framework Guide](/framework-guides) to decide which image you should pick.

Note: You may notice that some images say `Alpine` and some say `Debian`. This refers to the distribution of Linux that each of them is based on. As explained below, you usually want Alpine images.

Here are some general rules for picking images:

1. Don't pick the base Alpine or Debian images if you can help it. Try to pick an image that has what you need (for example, Python) already installed.
2. With Debian-based images, simple operations are orders of magnitude slower than with Alpine images. Debian images are an option in case you need them, but usually Alpine is fine.

#### `run.sh` templates

You may have noticed that some images say `Has run.sh template`, and under the image list, you see a checkbox labeled `Write run.sh file?`.

As described in [Site Processes](#site-processes) below, dynamic sites require a special file named `run.sh` that starts the site's server. Some of the Docker images you can choose from come with "templates" for your `run.sh` file, and checking this box when you update your site's image lets you use one of these templates as your site's `run.sh`.

In some cases, these templates will work out of the box; sometimes they require configuration. Again, we recommend you read the relevant [Framework Guide](/framework-guides).

**WARNING**: If you check the `Write run.sh file?` box but you have already set up a `run.sh` for your site, it will be overwritten. Be careful!

#### Extra packages

You can choose from a variety of images, but sometimes you need extra software installed. And if you just open up a terminal and tried to install something, you'll quickly discover that you can't edit anything outside of your site's main directory at `/site`. Unfortunately, making that possible would be very difficult to implement, so it is not supported.

However, the "Packages" textbox at the bottom of the page lets you install custom packages into your site's Docker image. Just enter a space-separated list of packages to install.

**WARNING**: If you make a typo and enter something that isn't the name of a real package, the process of building your site's Docker image will fail and a Director administrator will have to intervene to recover.

You can search for Alpine packages [here](https://pkgs.alpinelinux.org/packages?branch=edge&arch=x86_64), and you can search for Debian packages [here](https://www.debian.org/distrib/packages#search_packages).


## Site Processes

Dynamic sites require a special shell script named `run.sh` that starts the site's server.

In most cases, you will want to start with one of the default templates (see [`run.sh` templates](#runsh-templates) above). If you end up writing your own, the first line must be `#!/bin/sh` (NOT `#!/bin/bash`, unless you're using Debian or you specifically installed Bash).

Your site's `run.sh` can be located in any of the following places within your site's main directory (`/site` in the terminal):

- `run.sh`
- `private/run.sh`
- `public/run.sh`

Director goes down this list in order and uses the first one it finds.

Your `run.sh` file must also be marked as executable. To do this from the online editor, right click on it in the "Files" pane on the left and choose `Set executable`. If a file is executable, it will be colored green.

Once you've created a `run.sh` and set it as executable, you must restart your site for the changes to take effect.

Note: A previous version of Director allowed customizing the path of the script to run; however, this is not possible in current versions of Director. (Most people named their file `run.sh` and put it in one of these locations anyway.)

[^1]: <small>A Docker image is all the files for a particular OS and its setup; a Docker container is a running instance of an image. If you're familiar with virtual machines (VMs), a container is **conceptually similar to** a VM, and an image is like its hard drive.</small>
