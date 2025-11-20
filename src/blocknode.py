import re
from enum import StrEnum

from src.htmlnode import HTMLNode, LeafNode, ParentNode
from src.markdown_inline import to_textnodes
from src.textnode import TextNode, TextType

BlockType = StrEnum(
    "BlockType",
    ["PARAGRAPH", "HEADING", "CODE", "QUOTE", "UNORDERED_LIST", "ORDERED_LIST"],
)


class BlockNode:
    def __init__(self, markdown: str) -> None:
        self.block = re.sub(r"^\s*", "", markdown, flags=re.MULTILINE)
        self.block = re.sub(r"\n$", "", self.block)
        self.block_type = self._get_block_type()

    def to_html_node(self) -> HTMLNode:
        match self.block_type:
            case BlockType.HEADING:
                splits = self.block.split(" ")
                num = len(splits[0])
                value = " ".join(splits[1:])
                return ParentNode(f"h{num}", BlockNode._text_to_children(value))
            case BlockType.CODE:
                value = self.block.replace("```", "").lstrip("\n")
                return ParentNode("pre", [LeafNode("code", value)])
            case BlockType.QUOTE:
                block = re.sub(r">\s*", "", self.block, re.MULTILINE)
                values = BlockNode._text_to_children(block)
                return ParentNode("blockquote", values)
            case BlockType.UNORDERED_LIST | BlockType.ORDERED_LIST:
                block = (
                    re.sub(r"-\s", "", self.block)
                    if self.block_type == BlockType.UNORDERED_LIST
                    else re.sub(r"\d*\. ", "", self.block)
                )
                values = [
                    ParentNode("li", BlockNode._text_to_children(line))
                    for line in block.splitlines()
                ]
                return ParentNode(
                    "ul" if self.block_type == BlockType.UNORDERED_LIST else "ol",
                    values,
                )
            case BlockType.PARAGRAPH:
                values = BlockNode._text_to_children(self.block.replace("\n", " "))
                return ParentNode("p", values)

    @staticmethod
    def _text_to_children(block) -> list[LeafNode]:
        return [node.to_html_node() for node in to_textnodes([TextNode(block)])]

    def _get_block_type(self) -> BlockType:
        if re.match(r"#{1,6}\s", self.block):
            return BlockType.HEADING
        if self.block.startswith("```") and self.block.endswith("```"):
            return BlockType.CODE
        if all(line.startswith(">") for line in self.block.splitlines()):
            return BlockType.QUOTE
        if all(line.startswith("- ") for line in self.block.splitlines()):
            return BlockType.UNORDERED_LIST
        if all(re.match(r"^\d+\.\W", line) for line in self.block.splitlines()):
            if self._is_ordered_list():
                return BlockType.ORDERED_LIST
        return BlockType.PARAGRAPH

    def _is_ordered_list(self) -> bool:
        expected_num = 1
        for line in self.block.splitlines():
            if not line.startswith(f"{expected_num}. "):
                return False
            expected_num += 1
        return True

    def __eq__(self, value: object, /) -> bool:
        return (
            isinstance(value, BlockNode)
            and self.block == value.block
            and self.block_type == value.block_type
        )

    def __repr__(self) -> str:
        return f"BlockNode({self.block!r}, {self.block_type.value})"


# if __name__ == "__main__":
#     test_codeblock()
