#!/usr/bin/env python
"""Entry point for Literary corpus in Portuguese"""

import shutil
import tempfile
import logging
from  datetime import datetime

from typing import List, Union, Optional, Dict
from pathlib import Path
from tinydb import TinyDB, database, table, queries

from . import utils
from . import model


############################################################
# LOGGER SETTINGS
############################################################
logger: logging.Logger = logging.getLogger(__name__)

# Log file handler
logger_filename: str = 'litcorpt_debug.log'
logger_filepath: Path = utils.get_corpus_datapath() / logger_filename
logger_fd: logging.FileHandler = logging.FileHandler(logger_filepath)

# Log console handler
logger_console: logging.StreamHandler = logging.StreamHandler()

# Log formatting
# pylint: disable=line-too-long
formatstr: str = "%(asctime)s:%(module)s:%(filename)s:%(funcName)s:%(lineno)d:%(levelname)s:%(message)s"
logger_fmt: logging.Formatter = logging.Formatter(formatstr)

# Log settings
# INFO, WARN, ERROR, CRITICAL go to file
logger_fd.setFormatter(logger_fmt)
logger_fd.setLevel(logging.DEBUG)

# WARN, ERROR and CRITICAL go to console
logger_console.setFormatter(logger_fmt)
logger_console.setLevel(logging.DEBUG)

# Default logger
logger.setLevel(logging.DEBUG)
logger.addHandler(logger_console)
logger.addHandler(logger_fd)



def book_json_path(path: Union[str, Path]) -> Path:
    """Return a book's json path, from a dirpath

    Input:
        path: A dir path containing a book.

    Outputs:
        path: A file path pointing to  book json file (if exists).
    """
    path = Path(path)
    basename: str = path.name
    json_filepath: Path = path / f"{basename}.json"
    return json_filepath


def book_contents_path(path: Union[str, Path]) -> Path:
    """Return a book's json path, from a dirpath

    Input:
        path: A dir path containing a book.

    Outputs:
        path: A file path pointing to  book contents file (if exists).
    """
    path = Path(path)
    basename: str = path.name
    text_filepath: Path = path / f"{basename}.txt"
    return text_filepath


def book_read_json(path: Union[str, Path]) -> model.Book:
    """Read a book json file and returns as a Book """
    return model.Book.parse_file(path)


def book_read_contents(path: Union[str, Path]) -> str:
    """Read book contents from filepath"""
    with open(path, 'r') as contents_fd:
        contents: str = contents_fd.read()
    return contents


def book_read(path: Union[str, Path]) -> model.Book:
    """Read a book json and contents from file path and returns
    as a Book object. If a content text file exists at same
    dir, loads into Book.contents

    Input:
        path: A full path to book json file, or to dirpath where json is.

    Outputs:
        model.Book: A Book object
    """
    path = Path(path)
    basedir: Path
    json_filepath: Path
    text_filepath: Path

    if path.is_file():
        # We have a json filepath.
        basedir  = path.parent
        json_filepath = path
        text_filepath = book_contents_path(basedir)
    else:
        # We probably received a basedir
        basedir = path
        json_filepath = book_json_path(path)
        text_filepath = book_contents_path(path)

    # Righ now we have all information we need to read the data
    book: model.Book = book_read_json(json_filepath)
    if book.contents is None and text_filepath.exists():
        contents: str = book_read_contents(text_filepath)
        book.contents = contents

    return book


def book_write_contents(contents: Union[str, model.Book],
                        path: Path) -> None:
    """Writes book contents into filepath"""

    local_contents: Optional[str]

    if isinstance(contents, model.Book):
        local_contents = contents.contents
    elif isinstance(contents, str):
        local_contents = contents
    else:
        errmsg: str = f"contents: Expected Union[str, model.Book], but got {type(contents)}"
        raise TypeError(errmsg)

    with open(path, 'w') as contents_fd:
        contents_fd.write(str(local_contents))


def book_write_json(book: model.Book,
                    path: Union[str, Path],
                    with_contents=False) -> None:
    """Writes book json into filepath.

    Inputs:
        book: A book object

    Outputs:
    """
    json_args: Dict = {'indent': 2, 'ensure_ascii': True}
    model_args: Dict = {'exclude_none': True}
    book_json: str

    if not with_contents:
        book_json = book.json(exclude={'contents'}, **model_args, **json_args)
    else:
        book_json = book.json(indent=2, **model_args, **json_args)
    with open(path, 'w') as book_fp:
        book_fp.write(book_json)


def book_write(book: model.Book, path: Union[Path, str]) -> None:
    """Writes the Book object in a book dirpath. If book model contains
    the ebook content. It will write the json WITHOUT the contents and
    the contents into a different txt file at the same directory.

    Filenames will be fetched from latest directory in Path.

    For example:

    `book_write(book, '~/data/books/book123/')`

    It will create:

    ```
    ~/data/books/book123/book123.json
    ~/data/books/book123/book123.txt
    ```

    Directory '~/data/books/book123/' is created if does not exist, but
    if dirpath is a file. It raises an exception NotADirectoryError

    Inputs:
        book: The book to be written
        path: Location to write to.
    """
    # Ensures dirpath is a Path and expanded
    local_path: Path = Path(path).expanduser()

    if not local_path.exists():
        Path(local_path).mkdir(parents=True)
    elif not local_path.is_dir():
        raise NotADirectoryError(f"{path}")

    basename: str = local_path.name

    json_filepath: Path = local_path / f"{basename}.json"
    book_write_json(book=book, path=json_filepath, with_contents=False)

    text_filepath: Path = local_path / f"{basename}.txt"
    book_write_contents(contents=book, path=text_filepath)


def corpus_retrieve(corpus_datapath: Union[str, Path], corpus_url: str) -> None:
    """This function assures that corpus is available in CORPUS_DATAPATH.
    If not it will download it.
    """
    corpus_datapath = Path(corpus_datapath)
    checkin_file: Path = corpus_datapath / 'last.txt'
    logger.debug("Reading checkin file %s", checkin_file)
    if not checkin_file.exists():
        logger.info("START: Corpus retrieval.")
        logger.warning("Corpus not found in %s.", corpus_datapath)

        corpus_datapath.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory() as tmpdirname:
            # Build destination filepath
            filename: str = corpus_url.split('/')[-1]

            logger.warning("Downloading from %s.", corpus_url)
            logger.debug("Download destination %s/%s", tmpdirname, filename)
            # Download corpus
            filepath, _ = utils.download_file(corpus_url,
                                              dstdir=tmpdirname,
                                              filename=filename)

            logger.debug("Download finished %s", filepath)

            logger.info("Extracting zip to %s", corpus_datapath)

            # Extract Corpus
            shutil.unpack_archive(filepath, corpus_datapath, "zip")

        # Fill the success timestamp
        with open(checkin_file, 'w') as checkin_fd:
            now: datetime = datetime.now()
            timestamp: str = f'{now.year}{now.month}{now.day}{now.hour}{now.minute}{now.second}'
            checkin_fd.write(timestamp)

        logger.info("END: Corpus retrieval.")
    else:
        logger.info("Corpus found in %s.", corpus_datapath)

#%%
def corpus_read(path: Path) -> List[model.Book]:
    """Load corpus from corpus_path and return a list of Books

    The corpus_path must containg directories representing books
    as defined in book_read() function.
    """
    books: List[model.Book] = []
    for bookdir in path.iterdir():
        books.append(book_read(bookdir))

    return books

#%%
def corpus_write(corpus_data: List[model.Book],
                 path: Union[str, Path],
                 overwrite=False) -> List[bool]:
    """Write the whole corpus (a list of Books) into corpus_path.

    Inputs:
        corpus: A corpus structured as a List of model.Book objects.
        corpus_path: The dir path to corpus
        overwrite: Overwrite data if already exists.

    Outputs:
        status: A list with success status, related to each element in
                corpus input.
    """
    path = Path(path)
    write_status: List[bool] = []
    for book in corpus_data:
        bookpath: Path = path / book.index
        if bookpath.exists():
            if overwrite:
                # We need to catch some rmtree, add to failed status
                # and continue.
                shutil.rmtree(bookpath, ignore_errors=False, onerror=None)
            else:
                logger.warning("Book %s. Already exists. Skipping", book.index)
                write_status.append(False)
                continue

        # Here bookpath do not exists and we don't care for overwrite.
        try:
            book_write(book, bookpath)
        except NotADirectoryError as err:
            logger.warning("Book %s. Could not be written. %s", book.index, err)
            write_status.append(False)
        else:
            write_status.append(True)

    return write_status


def corpus_build_database(corpus_data: List[model.Book],
                          corpusdb_path: Union[str, Path]) -> database.TinyDB:
    """Returns the book database from a list of books"""

    corpusdb: database.TinyDB = TinyDB(corpusdb_path)

    logger.info("Building corpus %s with %d contents",
                corpusdb_path,
                len(corpus_data))

    corpusdb.insert_multiple(book.dict() for book in corpus_data)
    logger.info("Corpus completed with %d entries", len(corpusdb))

    return corpusdb


#%%
def corpus_load(rebuild: bool = False) -> database.TinyDB:
    """Load corpus. Download if needed. Returns the corpus database
    It loads the corpus from CORPUS_DATAPATH directory.

    Inputs:
        rebuild (Bool): Rebuild corpus.db even if it exists. Useful when
                        data is corrupted or was changed directly on file
                        (not so common).

    Outputs:
        corpus (database.TinyDB): Corpus as pandas dataframe or None
    """
    # Makes sure corpus if available
    corpus_datapath: Path = utils.get_corpus_datapath()
    corpus_url: str = utils.get_corpus_url()
    corpus_retrieve(corpus_datapath, corpus_url)

    # Resolve the zip file path.  zip dirname is: repository-branch
    datadir: str = 'litcorpt_data-main/data/'
    booksdir: Path = corpus_datapath / datadir

    # Corpus database file
    corpusdb_filename: str = 'corpus.db'
    corpusdb_filepath: Path = corpus_datapath / corpusdb_filename

    corpusdb: database.TinyDB
    if not corpusdb_filepath.exists() or rebuild:
        books = corpus_read(booksdir)
        corpusdb = corpus_build_database(books, corpusdb_filepath)
    else:
        logger.info("Loading corpus dataset %s", corpusdb_filepath)
        corpusdb = TinyDB(corpusdb_filepath)

    return corpusdb


#%%
def corpus(corpusdb: database.TinyDB,
           query: Optional[queries.QueryInstance] = None) -> List[str]:
    """Return a corpus list from corpusdb and a query (optional)

    Input:
        corpusdb (db): A Corpus database handler
        query (query): A query request. If no query is given, returns the whole corpus.

    Output:
        corpus (list): A list where each element is a document from corpus.
    """
    result: List[table.Document]
    if query is None:
        result = corpusdb.all()
    else:
        result = corpusdb.search(query)

    local_corpus: List[str] = [ entry.get('contents', '') for entry in result ]

    return local_corpus


#%%
def doc_id(corpusdb: database.TinyDB,
           query: Optional[queries.QueryInstance] = None) -> List[int]:
    """Return a list of document ids given a query

    Input:
        corpusdb (db): A Corpus database handler
        query (query): A query request. If no query is given, returns the whole corpus.

    Output:
        doc_ids (list): A list where each element is a document id from corpus.
    """
    result: List[table.Document]
    if query is None:
        result = corpusdb.all()
    else:
        result = corpusdb.search(query)

    doc_ids: List[int] = [ entry.doc_id for entry in result ]
    return doc_ids


#%%
if __name__ == '__main__':
    pass
