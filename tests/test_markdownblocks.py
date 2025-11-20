import unittest

from src.blocknode import BlockNode, BlockType
from src.markdown_blocks import markdown_to_blocks, markdown_to_html


class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        expected = [
            BlockNode("This is **bolded** paragraph"),
            BlockNode(
                "This is another paragraph with _italic_ text and `code` here\n"
                "This is the same paragraph on a new line"
            ),
            BlockNode("- This is a list\n- with items\n"),
        ]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_headers_and_spacing(self):
        md = """

        # Header Block

        This is a paragraph with text

        Another paragraph after extra spacing

        - item 1
        - item 2
        """
        blocks = markdown_to_blocks(md)
        expected = [
            BlockNode("# Header Block"),
            BlockNode("This is a paragraph with text"),
            BlockNode("Another paragraph after extra spacing"),
            BlockNode("- item 1\n- item 2\n"),
        ]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_code_and_lists(self):
        md = """
        Here is a paragraph before code:

        ```
        print("hello")
        print("world")
        ```


        1. First item
        2. Second item
        3. Third item
        """
        blocks = markdown_to_blocks(md)
        expected = [
            BlockNode("Here is a paragraph before code:"),
            BlockNode('```\nprint("hello")\nprint("world")\n```'),
            BlockNode("1. First item\n2. Second item\n3. Third item\n"),
        ]
        self.assertEqual(blocks, expected)

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        html = markdown_to_html(md).to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        html = markdown_to_html(md).to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading_levels(self):
        md = """
    # Heading One

    ## Heading Two

    ### Heading Three
    """
        html = markdown_to_html(md).to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading One</h1><h2>Heading Two</h2><h3>Heading Three</h3></div>",
        )

    def test_blockquote(self):
        md = """
    > This is a blockquote
    > with multiple lines
    """
        html = markdown_to_html(md).to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote\nwith multiple lines</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
    - item one
    - item two
    - item three
    """
        html = markdown_to_html(md).to_html()
        self.assertEqual(
            html,
            "<div><ul><li>item one</li><li>item two</li><li>item three</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
    1. first
    2. second
    3. third
    """
        html = markdown_to_html(md).to_html()
        self.assertEqual(
            html,
            "<div><ol><li>first</li><li>second</li><li>third</li></ol></div>",
        )

    def test_mixed_blocks(self):
        md = """
    # Title

    Paragraph with **bold** text.

    - item one
    - item two

    > quote line
    """
        html = markdown_to_html(md).to_html()
        self.assertEqual(
            html,
            "<div>"
            "<h1>Title</h1>"
            "<p>Paragraph with <b>bold</b> text.</p>"
            "<ul>"
            "<li>item one</li>"
            "<li>item two</li>"
            "</ul>"
            "<blockquote>quote line</blockquote>"
            "</div>",
        )

    def test_codeblock_inline_characters_unchanged(self):
        md = """
    ```
    keep _this_ **exactly** `as is`
    ```
    """
        html = markdown_to_html(md).to_html()
        self.assertEqual(
            html,
            "<div><pre><code>keep _this_ **exactly** `as is`\n</code></pre></div>",
        )

    def test_paragraph_with_newlines_kept_as_spaces(self):
        md = """
    This is a paragraph
    split across
    multiple lines
    """
        html = markdown_to_html(md).to_html()
        self.assertEqual(
            html,
            "<div><p>This is a paragraph split across multiple lines</p></div>",
        )


if __name__ == "__main__":
    unittest.main()
