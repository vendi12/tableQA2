# -*- coding: utf-8 -*-
'''
author: svakulenko
2 Aug 2017
'''

from elasticsearch import Elasticsearch

from load_csv import load_csv
from settings import *


def rows2ES(file_name, index_name, limit=2):
    '''
    Loads a table from the CSV file to the ES index row by row along with the heading within the row,
    i.e. row is a document to search for.
    '''

    es = Elasticsearch()

    # make sure the index exists
    # try:
    #     es.indices.delete(index=index_name)
    #     es.indices.create(index=index_name)
    # except:
    #     pass

    header, rows = load_csv(SAMPLE_CSV_FILE)
    row_strs = []
    if limit:
        rows = rows[:limit]
    for i, row in enumerate(rows):
        row_str = ""
        for j, cell in enumerate(row):
            # recursively append cells with headers
            row_str = "%s %s %s" % (row_str, header[j], cell)
        row_str = row_str.lower().strip()
        print row_str

        # write row to ES index
        es.index(index=index_name, doc_type=DOC_TYPE, id=i,
                 body={'content': row_str})


def test_rows2ES():
    rows2ES(SAMPLE_CSV_FILE, INDEX_NAME)


if __name__ == '__main__':
    test_rows2ES()
