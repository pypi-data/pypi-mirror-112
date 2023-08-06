from ebooklib import epub
from pathlib import Path

import click
import markdown
import re
import sys

@click.command()
@click.argument("filename")
def main(filename):
    chapters = split_chapters(filename)
    output_filename = Path(filename).stem + ".epub"
    build_epub(output_filename, chapters)

def split_chapters(filename):
    with open(filename, 'r') as file:
        content = file.read()

        pattern = re.compile("^第\d+章\s.*$", re.MULTILINE)
        headers = re.findall(pattern, content)
        bodies = re.split(pattern, content)[1:]
        chapters = list(zip(headers, bodies))

    return chapters

def build_epub(output_filename, chapters):
    book = epub.EpubBook()

    toc = []
    for title, body in chapters:
        match = re.search("第\d+章", title)
        if match:
            chapter_number = match.group()
        else:
            chapter_number = title

        html_chapter = epub.EpubHtml(
            title=title.strip(),
            file_name=chapter_number + '.xhtml'
        )

        chapter = "# " + title.strip() + "\n\n" + body.strip()
        html = markdown.markdown(chapter)
        html_chapter.content=html
        book.add_item(html_chapter)
        toc.append(html_chapter)

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    book.toc = toc
    book.spine = ['nav'] + toc
    epub.write_epub(output_filename, book, {})

if __name__ == '__main__':
    main()
