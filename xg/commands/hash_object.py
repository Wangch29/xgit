import hashlib
import sys
import zlib
from pathlib import Path

import typer
from typer import Argument, echo, Option
from typing_extensions import Annotated

from utils.repo import find_repo


def hash_object(
        file_path: Annotated[str, Argument(help="File to hash.")],
        write: Annotated[bool, Option("-w", "--write", help="Write the object into repo.")] = False
):
    """
    Calculate an object ID (SHA) and optionally write it to the object repo.
    """
    f = Path(file_path)
    if not f.is_file():
        echo(f"fatal: could not open '{f}' for reading: No such file or directory.", err=True)
        sys.exit(128)

    with f.open("rb") as f:
        data = f.read()

    object_data = b"blob" + b" " + str(len(data)).encode() + b"\x00" + data
    object_id = hashlib.sha1(object_data).hexdigest()

    typer.echo(object_id)

    if write:
        object_dir = find_repo() / ".git" / "objects" / object_id[:2]
        object_dir.mkdir(parents=True, exist_ok=True)
        with (object_dir / object_id[2:]).open("wb") as f:
            f.write(zlib.compress(object_data))
