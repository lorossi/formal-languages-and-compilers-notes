from pathlib import Path
from re import M, sub
from sys import argv

TEMP_FOLDERS = ["tikztemp"]
TEMP_EXTENSIONS = ["aux", "auxlock", "log", "pdf", "out", "toc"]
PLACEHOLDER_EXT = ".placeholder"
ARROW_STYLE = "{Triangle[scale=0.8]}"


def clean_styles() -> None:
    """cleans the tikzstyles file as it was created by tikzit"""
    # load styles files
    with open("tikzit.tikzstyles", "r") as f:
        data = f.read()

    # remove tikzit attributes
    data = sub("tikzit [a-z]+=(([a-zA-Z]+)|(\{.+\}))(, ){0,1}", "", data)
    # remove none fields
    data = sub("[a-z]*=none(, ){0,1}", "", data)
    # replace arrows
    data = sub("[<>]", ARROW_STYLE, data)
    # strip comments
    data = sub("^%.*\n", "", data, flags=M)
    # remove empty lines
    data = sub("^\s*$\n", "", data, flags=M)

    # save files
    with open("tikzstyle.tikzstyles", "w") as f:
        f.write(data)


def make_folder() -> None:
    for f in TEMP_FOLDERS:
        Path(f).mkdir(parents=True, exist_ok=True)
        Path(f"{f}/{PLACEHOLDER_EXT}").touch()


def delete_folder() -> None:
    for folder in TEMP_FOLDERS:
        for file in Path(folder).iterdir():
            file.unlink()
        Path(folder).rmdir()


def delete_temp() -> None:
    for e in TEMP_EXTENSIONS:
        for file in Path(".").glob(f"*.{e}"):
            file.unlink(missing_ok=True)


def main(argv: list[str]) -> None:
    if "deletetemp" in argv:
        delete_temp()
        delete_folder()
    if "cleanstyle" in argv:
        clean_styles()

    make_folder()


if __name__ == "__main__":
    main(argv)
