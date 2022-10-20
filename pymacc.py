import os
from dataclasses import dataclass
from pathlib import Path
import mistune


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


def main():
    body = "Content-Type: text/plain\n\n"
    path = "1"
    # request = Request(
    #     method=os.environ['REQUEST_METHOD'],
    #     uri=os.environ['REQUEST_URI'],
    #     scheme=os.environ['REQUEST_SCHEME'],
    #     remote_addr=os.environ['REMOTE_ADDR'],
    #     remote_port=int(os.environ['REMOTE_PORT']),
    #     hostname=os.environ['HTTP_HOST'],
    #     user_agent=os.environ['HTTP_USER_AGENT'],
    #     script_path=os.environ['SCRIPT_NAME'],
    # )
    # path = Path(request.script_path).parent() / request.uri
    body += f'path: {path}'
    print(body)


if __name__ == "__main__":
    main()
