#!/usr/bin/env python3
import os
import re
import time
import urllib.parse
import xml.etree.ElementTree
from typing import Any, Dict, Generator, Optional, Set, Tuple

import markdown
import markdown.extensions.toc
from flask import Flask, redirect


MARKDOWN_DIR = os.path.dirname(os.path.realpath(__file__))


app = Flask(__name__)


class LinkRewritingTreeProcessor(markdown.treeprocessors.Treeprocessor):
    def run(self, root: xml.etree.ElementTree.Element) -> None:
        self.handle_element(root)

    def handle_element(self, element: xml.etree.ElementTree.Element) -> None:
        # Handle children
        for child in element:
            self.handle_element(child)

        if element.tag == "a":
            href = element.get("href")
            if href is not None:
                parts = urllib.parse.urlsplit(href)

                # If it's not an external link, rewrite it
                if not parts.netloc:
                    # Extract the path for rewriting
                    path = parts.path

                    # Strip trailing slashes
                    path = path.rstrip("/")

                    # Remove .md suffixes
                    if path.endswith(".md"):
                        path = path[:-3]

                    path += "/"

                    # Recombine and use the new path
                    new_parts = (parts.scheme, parts.netloc, path, parts.query, parts.fragment)

                    # Update the element
                    element.set("href", urllib.parse.urlunsplit(new_parts))


class LinkRewritingExtension(markdown.extensions.Extension):
    def extendMarkdown(self, md: markdown.Markdown) -> None:
        md.treeprocessors.register(LinkRewritingTreeProcessor(md), "link_rewriter", -100)


def load_doc_page(page: str):
    # We do some checks that should prevent ".." attacks later, but
    # it's a good idea to check here too
    if ".." in page.split("/"):
        return {}, None

    page = page.rstrip("/")

    markdown_dir_clean = os.path.normpath(MARKDOWN_DIR)
    base_path = os.path.normpath(os.path.join(markdown_dir_clean, page))

    # Sanity check 1: Make sure they aren't trying to address a file outside the
    # directory.
    if os.path.commonpath([base_path, markdown_dir_clean]) != markdown_dir_clean:
        return {}, None

    # Sanity check 2: Don't allow loading hidden files.
    # This implicitly blocks ".." as well.
    for part in page.split("/"):
        if part.startswith("."):
            return {}, None

    # Render index.md within directories
    potential_paths = [
        base_path + ".md",
        os.path.join(base_path, "index.md"),
    ]

    for path in potential_paths:
        # Check if the path exists first
        if not os.path.exists(path):
            continue

        # Resolve symbolic links
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
                LinkRewritingExtension(),
            ],
        )

        text_html = markdown_converter.convert(text_md)
        metadata = markdown_converter.Meta  # pylint: disable=no-member

        return metadata, text_html

    return {}, None


PAGE_TITLE_REPLACE_RE = re.compile(r"[/-]+")
def get_page_title(page_name: str, metadata: Dict[str, Any]) -> str:
    if "title" in metadata:
        return " ".join(metadata["title"])
    elif page_name:
        return PAGE_TITLE_REPLACE_RE.sub(" ", page_name.strip("/-")).title()
    else:
        return "index"


@app.route("/")
@app.route("/<path:page>")
def serve(page: str = ""):
    if "//" in page or page.startswith("/") or (page and not page.endswith("/")):
        return redirect("/" + re.sub(r"/+", "/", page.strip("/")) + "/")

    metadata, text_html = load_doc_page(page)

    if text_html is None:
        return "Page not found", 404

    return """<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>{}</title>

    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>

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
</html>""".format(get_page_title(page, metadata), text_html)


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True, threaded=False)
