import re
from enum import StrEnum

from src.htmlnode import LeafNode

TextType = StrEnum("TextType", ["TEXT", "BOLD", "ITALIC", "CODE", "LINK", "IMAGE"])


class TextNode:
    def __init__(
        self, text: str, text_type: TextType = TextType.TEXT, url: str | None = None
    ) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def to_html_node(self) -> LeafNode:
        match self.text_type:
            case TextType.TEXT:
                return LeafNode(None, self.text)
            case TextType.BOLD:
                return LeafNode("b", self.text)
            case TextType.ITALIC:
                return LeafNode("i", self.text)
            case TextType.CODE:
                return LeafNode("code", self.text)
            case TextType.LINK:
                return LeafNode("a", self.text, {"href": self.url})
            case TextType.IMAGE:
                return LeafNode("img", "", {"src": self.url, "alt": self.text})

    def extract_markdown_images(self) -> list[tuple]:
        pat = r"!\[(.*?)]\((.*?)\)"
        return re.findall(pat, self.text)

    def extract_markdown_links(self) -> list[tuple]:
        pat = r"(?<!!)\[(.*?)]\((.*?)\)"
        return re.findall(pat, self.text)

    def __eq__(self, value: object, /) -> bool:
        return (
            isinstance(value, TextNode)
            and self.text == value.text
            and self.text_type == value.text_type
            and self.url == value.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text!r}, {self.text_type.value}, {self.url})"
