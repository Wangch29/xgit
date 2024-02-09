import sys
import zlib

from typer import Argument, echo, Option
from typing_extensions import Annotated

from utils.repo import find_repo


def cat_file(
        object_id: Annotated[str, Argument(help="File to hash.")],
        pretty: Annotated[bool, Option("-p", help="Pretty print the contents of the file.")] = False,
        show_size: Annotated[bool, Option("-s", help="Show file size.")] = False,
        show_type: Annotated[bool, Option("-t", help="Show file type.")] = False,
        exists: Annotated[bool, Option("-e", help="Exit with zero status if <object> exists and valid, "
                                                  "otherwise exit with non-zero")] = False
):
    """
    Display the contents of an object.
    """
    # One and only one of these options can be used at a time.
    if sum([pretty, show_size, show_type, exists]) != 1:
        echo("fatal: one and only one of -p, -s, -t, or -e can be used at a time.", err=True)
        sys.exit(129)

    file_path = find_repo() / ".git" / "objects" / object_id[:2] / object_id[2:]
    if not file_path.exists():
        if exists:
            sys.exit(1)
        echo(f"fatal: no such an object exists: {object_id}", err=True)
        sys.exit(128)

    with file_path.open("rb") as f:
        content = zlib.decompress(f.read())

    # <type> SPACE <size> "\0" <data>
    try:
        hdr, data = content.split(b"\x00", maxsplit=1)
        file_type, file_size = hdr.split(b" ", maxsplit=1)
    except ValueError:
        if exists:
            sys.exit(1)
        echo(f"fatal: invalid object", err=True)
        sys.exit(128)

    if exists:
        sys.exit(0)

    if show_type:
        echo(file_type.decode())

    if show_size:
        echo(file_size.decode())

    if pretty:
        if file_type == b"blob":
            echo(data.decode())
        else:
            raise NotImplementedError(f"pretty print of {file_type.decode()} not implemented.")
