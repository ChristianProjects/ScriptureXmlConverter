#!/usr/bin/env python3

from typing import List, Dict
from enum import Enum

class Format(Enum):
    OPENSONG_FORMAT = 'Opensong format'
    USX = 'usx'


class Loader:
    pass


class ScriptureVerse:
    index: int
    text: str

    def __init__(self, index: int, text: str):
        self.index = index
        self.text = text

class ScriptureChapter:
    index: int
    verses: List[ScriptureVerse]

    def __init__(self, index: int):
        self.index = index
        self.verses = []

class ScriptureBook:
    index: int
    name: str
    chapters: List[ScriptureChapter]
    
    def __init__(self, index: int, name: str):
        self.index = index
        self.name = name
        self.chapters = []

class ScriptureTree:
    books: List[ScriptureBook]
    
    def __init__(self):
        self.books = []  

class UsxFormatLoader(Loader):
    path: str
    _tree: ScriptureTree

    def __init__(self, path: str):
        self.path = path
    
    def load(self):
        '''
        loads `self.path` and converts it to a tree
        '''
        # open dir
        # traverse dir
        # for each file
        #   add a book
        #   traverse xml there and add chapters and for each chapter find just verses and text and add those
        #   this is it
        pass

    def tree(self):
        return self._tree

class Generator:
    pass

class OpensongFormatGenerator(Generator):
    tree: ScriptureTree

    def __init__(self, tree: ScriptureTree):
        self.tree = tree
    
    def generate(self, path: str):
        # generate with xml the actual text recursively
        # save into one file
        pass

def run(path: str, output_path: str, from_format: Format, to: Format):
    '''
    converts a file in `path` from `from_format` to `to` and saves it in `output_path`.
    currently only an usx -> Opensong convert is supported
    '''
    if from_format == Format.USX and to == Format.OPENSONG_FORMAT:
        loader = UsxFormatLoader(path)
        loader.load()
        generator = OpensongFormatGenerator(loader.tree())
        generator.generate(output_path)


if __name__ == '__main__':
    # TODO load args
    # converter.py <path> <output_path> <from> <to>
    path = 'tests/from'
    output_path = 'tests/to.xml'
    from_format = Format.USX_FORMAT
    to = Format.OPENSONG_FORMAT
    run(path, output_path, from_format, to)
