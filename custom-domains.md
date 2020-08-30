# Custom Domains

First, you will need to buy a domain name from a DNS provider, such as [Namecheap](https://namecheap.com) or [Pair Domains](https://pairdomains.com). (Note: These are not endorsements, just examples.)

Next, go to your provider's settings. It should show a list of DNS records. Add a new record. Choose the `CNAME` type and set the value to `user.tjhsst.edu`.

Note: In the past, hardcoding the IP with an `A` or `AAAA` entry would also have worked. However, things have changed and this is no longer the case. Please use a `CNAME`.

Finally, click the "Configure Site" button on your site's page and enter the name of your custom domain in one of the "Custom domain" boxes.
