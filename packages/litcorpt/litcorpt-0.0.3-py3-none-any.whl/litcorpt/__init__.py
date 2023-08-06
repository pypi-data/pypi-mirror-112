"""litcorpt module initialization"""

from tinydb import Query


__version__ = '0.0.3'
__author__ = 'Igor Morgado'
__author_email__ = 'morgado.igor@gmail.com'


from .main import (corpus,
                   corpus_load,
                   corpus_read,
                   corpus_write,
                   corpus_retrieve,
                   corpus_build_database,
                   book_write,
                   book_read,
                   doc_id,
                   logger,
)


# LATER: __all__ = [ ... ]
