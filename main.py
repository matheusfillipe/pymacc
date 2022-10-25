#!/usr/bin/env python3

import os
from dataclasses import dataclass
from pathlib import Path
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html
import mistune

BASE_URI = "/notes/"
ROOT_DIR = "www/"


formatter = html.HtmlFormatter(style="default")
HEAD = """
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, minimal-ui">
<meta name="color-scheme" content="light dark">
<link rel="stylesheet" href="github-markdown.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-fork-ribbon-css/0.2.3/gh-fork-ribbon.min.css">
<style>
			body {
				box-sizing: border-box;
				min-width: 200px;
				max-width: 980px;
				margin: 0 auto;
				padding: 45px;
			}

			@media (prefers-color-scheme: dark) {
				body {
					background-color: #0d1117;
				}
			}
		</style>
<style>
			.github-fork-ribbon:before {
				background-color: #121612;
			}
            pre {
                background-color: #282c34;
                overflow-x: auto;
                white-space: pre-wrap;
                white-space: -moz-pre-wrap;
                white-space: -pre-wrap;
                white-space: -o-pre-wrap;
                word-wrap: break-word;
                margin: 10px;
                padding: 10px;
            }
""" 

HEAD += formatter.get_style_defs()

HEAD += """
		</style>
"""


class HighlightRenderer(mistune.HTMLRenderer):
    def block_code(self, code, info=None):
        if info:
            lexer = get_lexer_by_name(info, stripall=True)
            return highlight(code, lexer, formatter)
        return '<pre><code>' + mistune.escape(code) + '</code></pre>'


markdown_gen = mistune.create_markdown(
    renderer=HighlightRenderer(),
    plugins=['url', 'table', 'footnotes', 'strikethrough', 'task_lists', 'def_list', 'abbr'])


@dataclass
class Request:
    method: str
    uri: str
    scheme: str
    remote_addr: str
    remote_port: int
    hostname: str
    user_agent: str
    script_path: str


def html_from_markdown(markdown, pgname):
    # Initialize html and import css
    generated_html = (
        "<!DOCTYPE html>"
        + "<html><head>"
        + "<title>{}</title>".format(pgname)
        + HEAD
        + "</head><body>"
    )

    generated_html += markdown_gen(markdown)
    generated_html += "</body></html>"
    return generated_html


def index(path=None):
    """"
    Loops through all the markdown files in the www directory recursively and create hyperlinks in a list.
    If a path is specified will list only the files in that directory or up until exists.
    """
    body = "<ul>"
    if path is None:
        for file in Path(ROOT_DIR).rglob("*.md"):
            body += f'<li><a href="{BASE_URI}/{file.relative_to(ROOT_DIR)}">{file.relative_to(ROOT_DIR)}</a></li>'
    else:
        directory = Path(ROOT_DIR + path)
        while not (directory.exists() and directory.is_dir()):
            directory = directory.parent
        for file in Path(directory).rglob("*.md"):
            body += f'<li><a href="{BASE_URI}/{file.relative_to(ROOT_DIR)}">{file.relative_to(ROOT_DIR)}</a></li>'

    body += "</ul>"
    return body


def main():
    body = "Content-Type: text/html\n\n"
    request = Request(
        method=os.environ['REQUEST_METHOD'],
        uri=os.environ['REQUEST_URI'],
        scheme=os.environ['REQUEST_SCHEME'],
        remote_addr=os.environ['REMOTE_ADDR'],
        remote_port=int(os.environ['REMOTE_PORT']),
        hostname=os.environ['HTTP_HOST'],
        user_agent=os.environ['HTTP_USER_AGENT'],
        script_path=os.environ['SCRIPT_FILENAME'],
    )

    path = request.uri.lstrip(BASE_URI)
    if path == "":
        body += "<h2>Index</h2>"
        body += index()
    else:
        try:
            with open(ROOT_DIR + path) as f:
                body += html_from_markdown("\n".join(f.readlines()),
                                           Path(path).stem)
        except (FileNotFoundError, IsADirectoryError):
            body += "<h2>Path not found</h2>"
            body += "<h3>Showing index instead</h3>"
            body += index(path)
    print(body)


if __name__ == "__main__":
    main()
