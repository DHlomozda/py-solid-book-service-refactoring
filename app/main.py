import json
import xml.etree.ElementTree as ElemT
from abc import ABC, abstractmethod


class ContentRenderer(ABC):
    @abstractmethod
    def render(self, content: str) -> None:
        pass


class ConsoleRenderer(ContentRenderer):
    def render(self, content: str) -> None:
        print(content)


class ReverseRenderer(ContentRenderer):
    def render(self, content: str) -> None:
        print(content[::-1])


class Book:
    def __init__(self, title: str, content: str) -> None:
        self.title = title
        self.content = content

    def display(self, renderer: ContentRenderer) -> None:
        renderer.render(self.content)
        # if display_type == "console":
        #     print(self.content)
        # elif display_type == "reverse":
        #     print(self.content[::-1])
        # else:
        #     raise ValueError(f"Unknown display type: {display_type}")

    def print_book(self, printer: ContentRenderer) -> None:
        print(f"Printing the book: {self.title}...")
        printer.render(self.content)
        # if print_type == "console":
        #     print(f"Printing the book: {self.title}...")
        #     print(self.content)
        # elif print_type == "reverse":
        #     print(f"Printing the book in reverse: {self.title}...")
        #     print(self.content[::-1])
        # else:
        #     raise ValueError(f"Unknown print type: {print_type}")


class Serializer(ABC):
    @abstractmethod
    def serialize(self, book: Book) -> str:
        pass


class JsonSerializer(Serializer):
    def serialize(self, book: Book) -> str:
        return json.dumps({"title": book.title, "content": book.content})


class XmlSerializer(Serializer):
    def serialize(self, book: Book) -> str:
        root = ElemT.Element("book")
        title = ElemT.SubElement(root, "title")
        title.text = book.title
        content = ElemT.SubElement(root, "content")
        content.text = book.content
        return ElemT.tostring(root, encoding="unicode")


def main(book: Book, commands: list[tuple[str, str]]) -> None | str:
    for cmd, method_type in commands:
        match cmd:
            case "display":
                if method_type == "console":
                    book.display(ConsoleRenderer())
                elif method_type == "reverse":
                    book.display(ReverseRenderer())
            case "print":
                if method_type == "console":
                    book.print_book(ConsoleRenderer())
                elif method_type == "reverse":
                    book.print_book(ReverseRenderer())
            case "serialize":
                if method_type == "json":
                    return JsonSerializer().serialize(book)
                elif method_type == "xml":
                    return XmlSerializer().serialize(book)
                else:
                    raise ValueError(f"Unknown method type: {method_type}")


if __name__ == "__main__":
    sample_book = Book("Sample Book", "This is some sample content.")
    print(main(sample_book, [("display", "reverse"), ("serialize", "xml")]))
