class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list | None = None,
        props: dict | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ""
        return f" {' '.join([f'{k}="{v}"' for k, v in self.props.items()])}"

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props}"


class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict | None = None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == "" and self.tag != "img":
            raise ValueError("All leaf nodes must have a value.")
        if self.tag is None or self.tag == "":
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list,
        props: dict | None = None,
    ) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == "":
            raise ValueError("All parent nodes must have a value.")
        if self.children is None or len(self.children) == 0:
            raise ValueError("All parent nodes must have children.")
        inner_html = ""
        for child in self.children:
            inner_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{inner_html}</{self.tag}>"
