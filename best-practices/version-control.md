# Version Control

We suggest using Git for version control. You can install Git by adding `git` to the list of packages to install in your Docker image by selecting "Customize Docker image" and adding it at the bottom of the page.

Some considerations:

* Static sites should not have the `public/` directory be the root of the `git` repository. The directory `public/.git` should not exist.
  As an alternative to making the `public/` directory the root directory, you can make the index folder (in the terminal, this is `/site/`) a Git repository.
  Generally, dynamic sites' `public/` directories can be the root of the `git` repository, except for sites such as PHP sites.

* If you require SSH (for Git over SSH), then you will also need the `openssh-client` package for an SSH client. Generate a private key using `ssh-keygen -t ed25519`, add it to your preferred
Git service, and you should be able to use Git for version control.

* In lieu of a webhook performing Git pulls, you will have to run `git pull` manually. There are currently no plans to integrate a webhook.
