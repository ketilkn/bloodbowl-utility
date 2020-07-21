import logging
import pathlib
import sys
import typing

LOG = logging.getLogger(__name__)


def load_raw(file_no) -> str:
    with open(file_no, mode='rb', closefd=False) as f:
        raw_input = f.read()
        try:
            return raw_input.decode('utf-8')
        except UnicodeDecodeError:
            return raw_input.decode('latin1')


def load_file(filename) -> str:
    the_path = pathlib.Path(filename)
    if the_path.is_file():
        with open(the_path, 'r') as f:
            return load_raw(f.fileno())


def load_document(document) -> str:
    if document == sys.stdin:
        return load_file(sys.stdin.fileno())
    else:
        return load_file(document)


def load_documents(documents) -> typing.Generator[str, None, None]:
    for document in documents:
        yield load_document(document)

