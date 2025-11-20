from src.blocknode import BlockNode
from src.htmlnode import ParentNode


def markdown_to_blocks(markdown: str) -> list[BlockNode]:
    return [BlockNode(m) for m in markdown.split("\n\n") if m.strip() != ""]


def markdown_to_html(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    html_nodes = [block.to_html_node() for block in blocks]
    return ParentNode("div", html_nodes)
