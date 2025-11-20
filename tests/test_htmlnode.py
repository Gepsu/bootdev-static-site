import unittest

from src.htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        props = HTMLNode(props={"href": "https://www.boot.dev", "target": "_blank"})
        self.assertEqual(
            props.props_to_html(), ' href="https://www.boot.dev" target="_blank"'
        )

    def test_props_to_html_empty(self):
        props = HTMLNode()
        self.assertEqual(props.props_to_html(), "")

    def test_props_to_html_empty_with_tag(self):
        props = HTMLNode(tag="h1", value="Hi")
        self.assertEqual(props.props_to_html(), "")

    def test_single_prop(self):
        props = HTMLNode(props={"class": "btn"})
        self.assertEqual(props.props_to_html(), ' class="btn"')


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_p_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://www.boot.dev">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hi!")
        self.assertEqual(node.to_html(), "Hi!")


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_multiple_children(self):
        child1 = LeafNode("p", "one")
        child2 = LeafNode("p", "two")
        parent_node = ParentNode("div", [child1, child2])
        self.assertEqual(parent_node.to_html(), "<div><p>one</p><p>two</p></div>")

    def test_empty_tag_raises_value_error(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("", [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_no_children_raises_value_error(self):
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_none_children_raises_value_error(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_child_leaf_without_tag(self):
        child_node = LeafNode(None, "text")
        parent_node = ParentNode("p", [child_node])
        self.assertEqual(parent_node.to_html(), "<p>text</p>")

    def test_deeply_nested_nodes(self):
        leaf = LeafNode("i", "deep")
        child = ParentNode("b", [leaf])
        parent = ParentNode("span", [child])
        grandparent = ParentNode("div", [parent])
        self.assertEqual(
            grandparent.to_html(), "<div><span><b><i>deep</i></b></span></div>"
        )

    def test_to_html_with_props(self):
        child = LeafNode("span", "child")
        parent = ParentNode("div", [child], props={"class": "container"})
        self.assertEqual(
            parent.to_html(), '<div class="container"><span>child</span></div>'
        )

    def test_to_html_with_multiple_props(self):
        child = LeafNode("b", "bold")
        parent = ParentNode(
            "div",
            [child],
            props={"class": "wrapper", "id": "main", "data-role": "content"},
        )
        self.assertEqual(
            parent.to_html(),
            '<div class="wrapper" id="main" data-role="content"><b>bold</b></div>',
        )

    def test_nested_nodes_with_props(self):
        child = LeafNode("i", "italic", props={"style": "color:red;"})
        parent = ParentNode("p", [child], props={"class": "text"})
        self.assertEqual(
            parent.to_html(), '<p class="text"><i style="color:red;">italic</i></p>'
        )


if __name__ == "__main__":
    unittest.main()
