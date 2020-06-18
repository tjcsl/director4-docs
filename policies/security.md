---
Title: Security
...

# Security

The Sysadmins reserve the right to disable without warning any site that does not follow these guidelines.

Administrators of all Director sites are responsible for ensuring that:

1. Their site follows appropriate security practices.
    - For example, Django sites should **never** have `DEBUG = True` set or be deployed with`./manage.py runserver`.
2. Their site does not allow access to CSL resources (such as eighth period signup information) by users who are not members of the TJ community.
3. Their site will never run arbitrary code received via its web interface without appropriately sandboxing said code.