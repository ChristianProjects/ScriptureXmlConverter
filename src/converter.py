#!/usr/bin/env python3

from typing import List, Dict, Optional
from enum import Enum
import os
import xml.etree.ElementTree as ET

class Format(Enum):
    OPENSONG_FORMAT = 'Opensong format'
    USX_FORMAT = 'usx'


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
    
    def load(self) -> None:
        '''
        loads `self.path` and converts it to a tree
        '''
        # open and traverse dir
        # for each file
        #   add a book
        #   traverse xml there and add chapters and for each chapter find just verses and text and add those
        #   this is it

        self._tree = ScriptureTree()

        for _, _, files in os.walk(self.path):
            for i, file in enumerate(sorted(files)):
                if file[0] != '0':
                    break
                book = self.load_book(i + 1, file)

                self._tree.books.append(book)
                break # TODO remove
        print(self._tree.books[0].chapters[0].verses[0].__dict__)

    def load_book(self, index: int, file: str) -> ScriptureBook:
        with open(os.path.join(self.path, file), 'r') as book_file:
            raw = book_file.read()

        xml = ET.fromstring(raw)

        # find title: first <para style="h">[title]</para>
        title_element = xml.find('para/[@style="h"]')
        if title_element is None:
            raise ValueError('expected title element')
        title = title_element.text
        book = ScriptureBook(index, title)
        print(book.__dict__)

        chapter_index = -1
        verses = []
        in_chapter = False
        verse_index = -1
        verse_text = ''
        for item in xml:
            if item.tag == 'chapter':
                if chapter_index != -1:
                    chapter_value = ScriptureChapter(chapter_index)
                    chapter_value.verses = verses
                    book.chapters.append(chapter_value)
                chapter_index = int(item.attrib['number'])
                in_chapter = True
                verses = []
            elif in_chapter and item.tag == 'para' and item.attrib['style'] == 'p':
                # print(item.text)
                # for raw_text in item.itertext():
                    # text = raw_text.strip()
                    # if len(text) > 0:
                        # print(text)
                for chapter_item in item:
                    if chapter_item.tag == 'verse':
                        if verse_index != -1:
                            verse_text = verse_text.strip()
                            verse_value = ScriptureVerse(verse_index, verse_text)
                            verses.append(verse_value)
                        verse_index = int(chapter_item.attrib['number'])
                        verse_text = ''
                    elif chapter_item.tag == None:
                        print(chapter_item)
                    elif chapter_item.tag == 'note' or chapter_item.tag == 'char':
                        if chapter_item.tag == 'char' and chapter_item.attrib['style'] in {'k', 'nd'}:
                            if chapter_item.text is not None:
                                verse_text + chapter_item.text + ' '
                        elif chapter_item.tag == 'char' and chapter_item.attrib['style'] == 'add':
                            # TODO: are those actually part of the Scripture?                            
                            if chapter_item.text is not None:
                                verse_text += '*' + chapter_item.text + '*'
                        if chapter_item.tail is not None and len(chapter_item) > 0:
                            verse_text += chapter_item.tail + ' '


                        # print(list(chapter_item.itertext()))
        if verse_index != -1:
            verse_text = verse_text.strip()
            verse_value = ScriptureVerse(verse_index, verse_text)
            verses.append(verse_value)
        if chapter_index != -1:
            chapter_value = ScriptureChapter(chapter_index)
            chapter_value.verses = verses
            book.chapters.append(chapter_value)
        return book

    def tree(self) -> ScriptureTree:
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
    if from_format == Format.USX_FORMAT and to == Format.OPENSONG_FORMAT:
        loader = UsxFormatLoader(path)
        loader.load()
        generator = OpensongFormatGenerator(loader.tree())
        generator.generate(output_path)


if __name__ == '__main__':
    # TODO load args
    # converter.py <path> <output_path> <from> <to>
    path = 'from' #'tests/from'
    output_path = 'to.xml' #'tests/to.xml'
    from_format = Format.USX_FORMAT
    to = Format.OPENSONG_FORMAT
    run(path, output_path, from_format, to)
