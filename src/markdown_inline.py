from src.textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        splits = node.text.split(delimiter)
        if len(splits) % 2 != 1:  # Len of splits should be odd
            raise ValueError("Invalid markdown syntax")
        for i, split in enumerate(splits):
            if split == "":
                continue
            new_nodes.append(
                TextNode(split, TextType.TEXT if i % 2 == 0 else text_type)
            )
    return new_nodes


def _split_nodes(old_nodes: list[TextNode], target_type: TextType) -> list[TextNode]:
    if target_type not in [TextType.IMAGE, TextType.LINK]:
        raise ValueError("Target type can only be IMAGE or LINK")

    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        is_image = target_type == TextType.IMAGE
        extract_func = (
            node.extract_markdown_images if is_image else node.extract_markdown_links
        )
        for alt, url in extract_func():
            sep = f"![{alt}]({url})" if is_image else f"[{alt}]({url})"
            splits = node.text.split(sep, 1)
            if splits[0] != "":
                new_nodes.append(TextNode(splits[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, target_type, url))
            node.text = "".join(splits[1:])
        if node.text != "":  # Text left or no image
            new_nodes.append(node)
    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes(old_nodes, TextType.IMAGE)


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes(old_nodes, TextType.LINK)


def to_textnodes(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = old_nodes.copy()
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes
