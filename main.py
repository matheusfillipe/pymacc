#!/usr/bin/env python3

import os
from dataclasses import dataclass
from pathlib import Path
import mistune

BASE_URI = "/notes/"
ROOT_DIR = "www/"


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

def html_from_markdown(markdown):
    generated_html = (
        "<!DOCTYPE html>"
        + "<html><head></head><body>"
    )

    generated_html += mistune.html(markdown)
    generated_html += "</body></html>"
    return generated_html

def index():
    """"
    Loops through all the markdown files in the www directory recursively and create hyperlinks in a list.
    """
    body = ""
    for file in Path(ROOT_DIR).rglob("*.md"):
        body += f'<a href="{file.relative_to(ROOT_DIR)}">{file.relative_to(ROOT_DIR)}</a><br>'
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
        body += index()
    else:
        with open(ROOT_DIR + path) as f:
            body += html_from_markdown("\n".join(f.readlines()))
    print(body)


if __name__ == "__main__":
    main()
