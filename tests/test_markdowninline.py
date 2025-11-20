import unittest

from src.markdown_inline import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    to_textnodes,
)
from src.textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            split_nodes_image([node]),
        )

    def test_split_links(self):
        node = TextNode(
            "This is a text with a [link](https://google.com) and another [Boot.dev](https://boot.dev)",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("This is a text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("Boot.dev", TextType.LINK, "https://boot.dev"),
            ],
            split_nodes_link([node]),
        )

    def test_split_images_no_images(self):
        node = TextNode("This text has no images.", TextType.TEXT)
        self.assertListEqual(
            [TextNode("This text has no images.", TextType.TEXT)],
            split_nodes_image([node]),
        )

    def test_split_images_at_start(self):
        node = TextNode("![alt text](url.com/img.png) is the image", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("alt text", TextType.IMAGE, "url.com/img.png"),
                TextNode(" is the image", TextType.TEXT),
            ],
            split_nodes_image([node]),
        )

    def test_split_images_at_end(self):
        node = TextNode("The image is here ![pic](url.com/pic.png)", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("The image is here ", TextType.TEXT),
                TextNode("pic", TextType.IMAGE, "url.com/pic.png"),
            ],
            split_nodes_image([node]),
        )

    def test_split_images_multiple_nodes(self):
        nodes = [
            TextNode("Here is ![one](url1)", TextType.TEXT),
            TextNode("and ![two](url2) here", TextType.TEXT),
        ]
        self.assertListEqual(
            [
                TextNode("Here is ", TextType.TEXT),
                TextNode("one", TextType.IMAGE, "url1"),
                TextNode("and ", TextType.TEXT),
                TextNode("two", TextType.IMAGE, "url2"),
                TextNode(" here", TextType.TEXT),
            ],
            split_nodes_image(nodes),
        )

    def test_split_images_ignores_non_text_nodes(self):
        nodes = [
            TextNode("![a](url)", TextType.TEXT),
            TextNode("![b](url2)", TextType.BOLD),
        ]
        self.assertListEqual(
            [
                TextNode("a", TextType.IMAGE, "url"),
                TextNode("![b](url2)", TextType.BOLD),
            ],
            split_nodes_image(nodes),
        )

    def test_split_links_no_links(self):
        node = TextNode("Nothing here!", TextType.TEXT)
        self.assertListEqual(
            [TextNode("Nothing here!", TextType.TEXT)],
            split_nodes_link([node]),
        )

    def test_split_links_at_start(self):
        node = TextNode("[start](url.com) is first", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("start", TextType.LINK, "url.com"),
                TextNode(" is first", TextType.TEXT),
            ],
            split_nodes_link([node]),
        )

    def test_split_links_at_end(self):
        node = TextNode(
            "Click this [end](url)",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("Click this ", TextType.TEXT),
                TextNode("end", TextType.LINK, "url"),
            ],
            split_nodes_link([node]),
        )

    def test_split_links_multiple_nodes(self):
        nodes = [
            TextNode("A [one](u1)", TextType.TEXT),
            TextNode("B [two](u2) C", TextType.TEXT),
        ]
        self.assertListEqual(
            [
                TextNode("A ", TextType.TEXT),
                TextNode("one", TextType.LINK, "u1"),
                TextNode("B ", TextType.TEXT),
                TextNode("two", TextType.LINK, "u2"),
                TextNode(" C", TextType.TEXT),
            ],
            split_nodes_link(nodes),
        )

    def test_split_links_ignores_non_text_nodes(self):
        nodes = [
            TextNode("[yes](url)", TextType.TEXT),
            TextNode("[nope](ignored.com)", TextType.ITALIC),
        ]
        self.assertListEqual(
            [
                TextNode("yes", TextType.LINK, "url"),
                TextNode("[nope](ignored.com)", TextType.ITALIC),
            ],
            split_nodes_link(nodes),
        )

    def test_split_links_mixed_with_images(self):
        node = TextNode(
            "Here is [link](u1) and ![img](u2)",
            TextType.TEXT,
        )
        result = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("Here is ", TextType.TEXT),
                TextNode("link", TextType.LINK, "u1"),
                TextNode(" and ![img](u2)", TextType.TEXT),
            ],
            result,
        )

    def test_split_to_all_types(self):
        node = TextNode(
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
            TextType.TEXT,
        )
        result = to_textnodes([node])

        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            result,
        )

    def test_to_textnodes_no_formatting(self):
        node = TextNode("Just plain text here", TextType.TEXT)
        self.assertListEqual(
            [TextNode("Just plain text here", TextType.TEXT)],
            to_textnodes([node]),
        )

    def test_to_textnodes_only_bold(self):
        node = TextNode("Hello **world**!", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("Hello ", TextType.TEXT),
                TextNode("world", TextType.BOLD),
                TextNode("!", TextType.TEXT),
            ],
            to_textnodes([node]),
        )

    def test_to_textnodes_italic_and_bold_mix(self):
        node = TextNode("Mix of _italic_ and **bold** text", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("Mix of ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
            to_textnodes([node]),
        )

    def test_to_textnodes_code_inside_bold(self):
        node = TextNode("Bold with `code` inside **bold**", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("Bold with ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" inside ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
            ],
            to_textnodes([node]),
        )

    def test_to_textnodes_link_before_italic(self):
        node = TextNode("[Link](url.com) and then _italic_", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("Link", TextType.LINK, "url.com"),
                TextNode(" and then ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            to_textnodes([node]),
        )

    def test_to_textnodes_image_and_code(self):
        node = TextNode("Here is `code` and an ![img](x.png)", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("Here is ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "x.png"),
            ],
            to_textnodes([node]),
        )

    def test_to_textnodes_multiple_nodes(self):
        nodes = [
            TextNode("**A**", TextType.TEXT),
            TextNode("then _B_", TextType.TEXT),
        ]
        self.assertListEqual(
            [
                TextNode("A", TextType.BOLD),
                TextNode("then ", TextType.TEXT),
                TextNode("B", TextType.ITALIC),
            ],
            to_textnodes(nodes),
        )

    def test_to_textnodes_image_then_link(self):
        node = TextNode("![alt](img.png) and [link](url)", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("alt", TextType.IMAGE, "img.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
            ],
            to_textnodes([node]),
        )

    def test_to_textnodes_multiple_images_and_bold(self):
        node = TextNode(
            "![a](1.png) and **bold** and ![b](2.png)",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("a", TextType.IMAGE, "1.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("b", TextType.IMAGE, "2.png"),
            ],
            to_textnodes([node]),
        )

    def test_to_textnodes_only_code(self):
        node = TextNode("`x = 1`", TextType.TEXT)
        self.assertListEqual(
            [TextNode("x = 1", TextType.CODE)],
            to_textnodes([node]),
        )

    def test_to_textnodes_empty_string(self):
        node = TextNode("", TextType.TEXT)
        self.assertListEqual([], to_textnodes([node]))

    def test_to_textnodes_preserves_non_text_nodes(self):
        nodes = [
            TextNode("**bold**", TextType.TEXT),
            TextNode("already italic", TextType.ITALIC),
        ]
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode("already italic", TextType.ITALIC),
            ],
            to_textnodes(nodes),
        )

    def test_split_delimiter_code(self):
        node = TextNode("`This is` text with a ` code block` word", TextType.TEXT)
        expected = [
            TextNode("This is", TextType.CODE),
            TextNode(" text with a ", TextType.TEXT),
            TextNode(" code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), expected)

    def test_split_multiple_nodes(self):
        nodes = [
            TextNode("Before `code`", TextType.TEXT),
            TextNode("More `stuff` here", TextType.TEXT),
        ]
        expected = [
            TextNode("Before ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode("More ", TextType.TEXT),
            TextNode("stuff", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "`", TextType.CODE), expected)

    def test_split_unbalanced_raises(self):
        node = TextNode("This `is broken", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_split_ignores_non_text_nodes(self):
        nodes = [
            TextNode("`code` here", TextType.TEXT),
            TextNode("bold stays same", TextType.BOLD),
        ]
        expected = [
            TextNode("code", TextType.CODE),
            TextNode(" here", TextType.TEXT),
            TextNode("bold stays same", TextType.BOLD),
        ]

        self.assertEqual(split_nodes_delimiter(nodes, "`", TextType.CODE), expected)

    def test_split_empty_between_delimiters(self):
        node = TextNode("Here is `` empty `` code", TextType.TEXT)
        expected = [
            TextNode("Here is ", TextType.TEXT),
            TextNode(" empty ", TextType.TEXT),
            TextNode(" code", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), expected)

    def test_split_no_delimiter(self):
        node = TextNode("Nothing to change", TextType.TEXT)
        expected = [TextNode("Nothing to change", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), expected)

    def test_split_bold_basic(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), expected)

    def test_split_bold_multiple(self):
        node = TextNode("**A** and **B**", TextType.TEXT)
        expected = [
            TextNode("A", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("B", TextType.BOLD),
        ]
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), expected)

    def test_split_italic_basic(self):
        node = TextNode("This *word* is italic", TextType.TEXT)
        expected = [
            TextNode("This ", TextType.TEXT),
            TextNode("word", TextType.ITALIC),
            TextNode(" is italic", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([node], "*", TextType.ITALIC), expected)

    def test_split_italic_multiple_with_underscore(self):
        node = TextNode("_A_ and _B_ are italic", TextType.TEXT)
        expected = [
            TextNode("A", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("B", TextType.ITALIC),
            TextNode(" are italic", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([node], "_", TextType.ITALIC), expected)

    def test_split_italic_unbalanced(self):
        node = TextNode("This *is broken", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "*", TextType.ITALIC)


if __name__ == "__main__":
    unittest.main()
