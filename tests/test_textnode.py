import unittest

from src.textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.node_a = TextNode("This is a text node", TextType.BOLD)

    def test_equals(self):
        node_b = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(self.node_a, node_b)

    def test_different_texttype(self):
        node_b = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(self.node_a, node_b)

    def test_different_text(self):
        node_b = TextNode("This is a text node, but different", TextType.BOLD)
        self.assertNotEqual(self.node_a, node_b)

    def test_additional_url(self):
        node_b = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        self.assertNotEqual(self.node_a, node_b)

    def test_convert_bold(self):
        node = TextNode("bold text", TextType.BOLD)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold text")

    def test_convert_italic(self):
        node = TextNode("italic text", TextType.ITALIC)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "italic text")

    def test_convert_code(self):
        node = TextNode("print('hi')", TextType.CODE)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hi')")

    def test_convert_link(self):
        node = TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev")
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Boot.dev")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})

    def test_convert_image(self):
        node = TextNode("alt text", TextType.IMAGE, "img/test.png")
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "img/test.png", "alt": "alt text"},
        )

    def test_convert_text(self):
        node = TextNode("Just text", TextType.TEXT)
        html_node = node.to_html_node()
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "Just text")

    def test_extract_markdown_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        self.assertListEqual(
            node.extract_markdown_images(),
            [("image", "https://i.imgur.com/zjjcJKZ.png")],
        )

    def test_extract_multiple_markdown_images(self):
        node = TextNode(
            "Here is ![img1](url1.png) and here is ![img2](url2.jpg)",
            TextType.TEXT,
        )
        self.assertListEqual(
            node.extract_markdown_images(),
            [
                ("img1", "url1.png"),
                ("img2", "url2.jpg"),
            ],
        )

    def test_extract_markdown_links_basic(self):
        node = TextNode(
            "Visit [Boot.dev](https://www.boot.dev) for learning.",
            TextType.TEXT,
        )
        self.assertListEqual(
            node.extract_markdown_links(),
            [("Boot.dev", "https://www.boot.dev")],
        )

    def test_extract_image_and_link_separately(self):
        node = TextNode(
            "Here is ![img](img.png) and a link: [Boot.dev](https://boot.dev)",
            TextType.TEXT,
        )
        self.assertListEqual(node.extract_markdown_images(), [("img", "img.png")])
        self.assertListEqual(
            node.extract_markdown_links(), [("Boot.dev", "https://boot.dev")]
        )


if __name__ == "__main__":
    unittest.main()
