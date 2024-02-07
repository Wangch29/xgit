from pathlib import Path
import sys

from typer import Argument, echo
from typing_extensions import Annotated, Optional


def init(directory: Annotated[str, Argument(help="Directory to initialize.")] = "."):
    """ Initialize a new project. """
    git_dir = Path(directory) / ".git"

    if git_dir.exists():
        echo(f"fatal: git repo \"{git_dir.absolute()}\" already exists, skipping...", err=True)
        sys.exit(1)

    git_dir.mkdir(parents=True, exist_ok=False)

    (git_dir / "objects").mkdir(parents=True, exist_ok=False)
    (git_dir / "refs" / "heads").mkdir(parents=True, exist_ok=False)
    (git_dir / "refs" / "tags").mkdir(parents=True, exist_ok=False)

    with (git_dir / "HEAD").open("w") as f:
        f.write("ref: refs/heads/main\n")

    echo(f"Initializing empty Xgit repo in \"{git_dir.absolute()}\"")
