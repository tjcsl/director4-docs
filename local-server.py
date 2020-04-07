#!/usr/bin/env python3
import os
import re
import time
import urllib.parse
import xml.etree.ElementTree
from typing import Any, Dict, Generator, Optional, Set, Tuple

import bleach
import markdown
import markdown.extensions.toc
from flask import Flask, redirect, send_file


MARKDOWN_DIR = os.path.dirname(os.path.realpath(__file__))


# Based off of https://github.com/yourcelf/bleach-whitelist/blob/1b1d5bbced6fa9d5342380c68a57f63720a4d01b/bleach_whitelist/bleach_whitelist.py
ALLOWED_TAGS = [
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "b",
    "i",
    "strong",
    "em",
    "tt",
    "p",
    "br",
    "span",
    "div",
    "blockquote",
    "code",
    "hr",
    "ul",
    "ol",
    "li",
    "dd",
    "dt",
    "img",
    "a",
    "sub",
    "sup",
    "small",
    "pre",
]

ALLOWED_ATTRS = {
    "*": ["id"],
    "img": ["src", "alt", "title"],
    "a": ["href", "title"],
}

ALLOWED_STYLES = []

cleaner = bleach.sanitizer.Cleaner(
    tags=ALLOWED_TAGS,
    attributes=ALLOWED_ATTRS,
    styles=ALLOWED_STYLES,
    strip=True,
    strip_comments=True,
)

app = Flask(__name__)


class LinkRewritingTreeProcessor(markdown.treeprocessors.Treeprocessor):
    def __init__(self, md: markdown.Markdown, page: str) -> None:
        super().__init__(md)
        self.page = page.strip("/")

    def run(self, root: xml.etree.ElementTree.Element) -> None:
        self.handle_element(root)

    def handle_element(self, element: xml.etree.ElementTree.Element) -> None:
        # Handle children
        for child in element:
            self.handle_element(child)

        if element.tag == "a":
            href = element.get("href")
            if href is not None:
                element.set("href", rewrite_markdown_link(link_url=href, base_page_name=self.page))


class LinkRewritingExtension(markdown.extensions.Extension):
    def __init__(self, page: str) -> None:
        self.page = page

    def extendMarkdown(self, md: markdown.Markdown) -> None:
        md.treeprocessors.register(LinkRewritingTreeProcessor(md, self.page), "link_rewriter", -100)


def rewrite_markdown_link(*, link_url: str, base_page_name: str) -> str:
    parts = urllib.parse.urlsplit(link_url)

    base_page_name = base_page_name.strip("/")

    # If it's not an external link, rewrite it
    if not parts.netloc and parts.path:
        # Extract the path for rewriting
        path = parts.path

        ext = os.path.splitext(path)[1]
        if not ext or ext == ".md":
            # If there's no file extension, or if it's a link to a markdown file

            if ext == ".md":
                # Remove .md suffixes
                path = path[:-3]

            # Ensure we have exactly one trailing slash
            path = path.rstrip("/") + "/"

        # For other file extensions, do nothing. In particular, no trailing slash.

        if not path.startswith("/"):
            # Make the path absolute by combining with the previous page

            # Remove the last portion and combine with the rest
            if "/" in base_page_name:
                parent_page = base_page_name.rsplit("/", 1)[0]
            else:
                parent_page = ""

            path = os.path.normpath(os.path.join("/", parent_page, path))

        # Recombine and use the new path
        new_parts = (parts.scheme, parts.netloc, path, parts.query, parts.fragment)

        return urllib.parse.urlunsplit(new_parts)
    else:
        return link_url


def url_to_path(url: str) -> Optional[str]:
    # We do some checks that should prevent ".." attacks later, but
    # it's a good idea to check here too
    if ".." in url.split("/"):
        return None

    url = url.rstrip("/")

    markdown_dir_clean = os.path.normpath(MARKDOWN_DIR)
    base_path = os.path.normpath(os.path.join(markdown_dir_clean, url))

    # Sanity check 1: Make sure they aren't trying to address a file outside the
    # directory.
    if os.path.commonpath([base_path, markdown_dir_clean]) != markdown_dir_clean:
        return None

    # Sanity check 2: Don't allow loading hidden files.
    # This implicitly blocks ".." as well.
    for part in url.split("/"):
        if part.startswith("."):
            return None

    return base_path


def load_doc_page(page: str):
    base_path = url_to_path(page)
    if base_path is None:
        return {}, None

    markdown_dir_clean = os.path.normpath(MARKDOWN_DIR)

    # Render index.md within directories
    potential_paths = [
        (base_path + ".md", ""),
        (os.path.join(base_path, "index.md"), "index"),
    ]

    for path, extra_part in potential_paths:
        # We add on the "extra part" because if this was a file like /a/index.md,
        # then links should be interpreted relative to /a.
        # If it was just /a.md, they should be interpreted relative to /.
        base_page_name = (page + "/" + extra_part).rstrip("/")

        # Check if the path exists first
        if not os.path.exists(path):
            continue

        # Treat symlinks as redirects
        if os.path.islink(path):
            redirect_url = rewrite_markdown_link(
                link_url=os.readlink(path),
                base_page_name=base_page_name,
            )

            return {"Redirect": redirect_url}, ""

        # Resolve symbolic links in other parts of the path
        path = os.path.realpath(path)

        # Don't render READMEs
        fname = os.path.basename(path)
        if fname == "README.md":
            continue

        # And check that the path is still within the directory
        if os.path.commonpath([path, markdown_dir_clean]) != markdown_dir_clean:
            continue

        with open(path) as f_obj:
            text_md = f_obj.read()

        # Render as HTML
        markdown_converter = markdown.Markdown(
            extensions=[
                "fenced_code",
                "footnotes",
                "tables",
                "meta",
                "nl2br",
                markdown.extensions.toc.TocExtension(),
                LinkRewritingExtension(base_page_name),
            ],
            tab_length=4,
            output_format="html5",
        )

        text_html = cleaner.clean(markdown_converter.convert(text_md))

        metadata = markdown_converter.Meta  # pylint: disable=no-member

        return metadata, text_html

    return {}, None


def find_static_file(url: str) -> Optional[str]:
    base_path = url_to_path(url)
    if base_path is None:
        return None

    markdown_dir_clean = os.path.normpath(MARKDOWN_DIR)

    if os.path.commonpath([base_path, markdown_dir_clean]) != markdown_dir_clean:
        return None

    return base_path


PAGE_TITLE_REPLACE_RE = re.compile(r"[/-]+")
def get_page_title(page_name: str, metadata: Dict[str, Any]) -> str:
    if "title" in metadata:
        return " ".join(metadata["title"])
    elif page_name:
        return PAGE_TITLE_REPLACE_RE.sub(" ", page_name.strip("/-")).title()
    else:
        return "index"


@app.route("/")
@app.route("/<path:url>")
def serve(url: str = ""):
    ext = os.path.splitext(url)[1]

    if ext == ".md":
        return redirect("/" + url[:-3] + "/")
    elif ext:
        fpath = find_static_file(url)
        if fpath is not None and os.path.isfile(fpath):
            return send_file(fpath)


    if "//" in url or url.startswith("/"):
        return redirect("/" + re.sub(r"/+", "/", url.strip("/")) + "/")

    if not ext and url and not url.endswith("/"):
        return redirect("/" + url + "/")

    metadata, text_html = load_doc_page(url)

    if text_html is None:
        return "Page not found", 404

    if metadata.get("Redirect"):
        return redirect("/" + metadata.get("Redirect").lstrip("/"))

    if url and not url.endswith("/"):
        return redirect("/" + url + "/")

    return """<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>{}</title>

    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">

    <script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>

    <link rel="stylesheet"
          href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.18.1/styles/default.min.css"
          integrity="sha256-zcunqSn1llgADaIPFyzrQ8USIjX2VpuxHzUwYisOwo8= sha512-h0/Zh3Xv/rDANm6S9yRPeNMHQVIy3f0VcvLGfJFeEOibLcHDadiHyqlb2+FjiwDLIGwluKRhxh1cqUYpGoj/yw=="
          crossorigin="anonymous">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.18.1/highlight.min.js"
            integrity="sha256-eOgo0OtLL4cdq7RdwRUiGKLX9XsIJ7nGhWEKbohmVAQ= sha512-1LdB3V708w6G4QRl7NsVdTr7MDibyRXr9stQZ+EGjEE0ZPMZkA//ir7kCWmFyxdAJNIRXdR/ZeJmCV0boyiCXw=="
            crossorigin="anonymous"></script>
    <script>hljs.initHighlightingOnLoad();</script>

    <style>
        body {{
            font-family: 'Open Sans', sans-serif;
            color: #24292e;
            background-color: #fff;
            margin: 15px 26px 26px 26px;
        }}

        a {{
            color: #007bff;
            text-decoration: none;
            background-color: transparent;
        }}
        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
{}
</body>
</html>""".format(get_page_title(url, metadata), text_html)


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True, threaded=False)
