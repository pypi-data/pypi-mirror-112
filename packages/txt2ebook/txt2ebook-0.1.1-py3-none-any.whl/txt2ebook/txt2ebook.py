from ebooklib import epub
from pathlib import Path
from pprint import pprint

import click
import logging
import markdown
import os
import re
import sys

logging.basicConfig(
    level=os.environ.get("LOG", "INFO").upper(),
    format="[%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


@click.command()
@click.argument("filename")
def main(filename):
    try:
        logger.debug(f"Processing txt file: '{filename}'")
        chapters = split_chapters(filename)
        output_filename = Path(filename).stem + ".epub"
        build_epub(output_filename, chapters)

    except FileNotFoundError as e:
        raise SystemExit(f"Error: {e.strerror}: '{filename}'")

    except Exception as e:
        raise SystemExit(e)


def split_chapters(filename):
    with open(filename, 'r') as file:
        content = file.read()

        if not content:
            raise Exception(f"Error: Empty file content in '{filename}'")

        pattern = re.compile(r"^第\d+章\s.*$", re.MULTILINE)
        headers = re.findall(pattern, content)

        if not headers:
            raise Exception(f"Error: No chapter headers found in '{filename}'")

        bodies = re.split(pattern, content)
        chapters = list(zip(headers, bodies[1:]))

    return chapters


def build_epub(output_filename, chapters):
    book = epub.EpubBook()

    toc = []
    for title, body in chapters:
        title = title.strip()
        body = body.strip()
        match = re.search(r"第\d+章", title)
        if match:
            filename = match.group()
        else:
            filename = title

        logger.debug(title)
        html_chapter = epub.EpubHtml(
            title=title,
            file_name=filename + '.xhtml'
        )

        chapter = "# " + title + "\n\n" + body
        html = markdown.markdown(chapter)
        html_chapter.content = html
        book.add_item(html_chapter)
        toc.append(html_chapter)

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    book.toc = toc
    book.spine = ['nav'] + toc

    logger.debug(f"Generating epub file: '{output_filename}'")
    epub.write_epub(output_filename, book, {})


if __name__ == '__main__':
    main()
