import unittest

from src.blocknode import BlockNode, BlockType


class TestBlockNode(unittest.TestCase):
    def test_ordered_list_valid(self):
        block = BlockNode("1. First\n2. Second\n3. Third")
        html = block.to_html_node().to_html()
        self.assertEqual(block.block_type, BlockType.ORDERED_LIST)
        self.assertEqual(html, "<ol><li>First</li><li>Second</li><li>Third</li></ol>")

    def test_ordered_list_with_fancies(self):
        block = BlockNode("1. **First**\n2. _Second_")
        html = block.to_html_node().to_html()
        self.assertEqual(block.block_type, BlockType.ORDERED_LIST)
        self.assertEqual(html, "<ol><li><b>First</b></li><li><i>Second</i></li></ol>")

    def test_ordered_list_invalid_numbers(self):
        block = BlockNode("1. First\n3. Third")
        self.assertEqual(block.block_type, BlockType.PARAGRAPH)

    def test_ordered_list_non_integer(self):
        block = BlockNode("1. First\nTwo. Second")
        self.assertEqual(block.block_type, BlockType.PARAGRAPH)

    def test_ordered_list_missing_period(self):
        block = BlockNode("1 First\n2. Second")
        self.assertEqual(block.block_type, BlockType.PARAGRAPH)

    def test_ordered_list_single_item(self):
        block = BlockNode("1. Only item")
        html = block.to_html_node().to_html()
        self.assertEqual(block.block_type, BlockType.ORDERED_LIST)
        self.assertEqual(html, "<ol><li>Only item</li></ol>")

    def test_unordered_list_valid(self):
        block = BlockNode("- a\n- b\n- c")
        html = block.to_html_node().to_html()
        self.assertEqual(block.block_type, BlockType.UNORDERED_LIST)
        self.assertEqual(html, "<ul><li>a</li><li>b</li><li>c</li></ul>")

    def test_unordered_list_mixed_invalid(self):
        block = BlockNode("- a\n2. b")
        self.assertEqual(block.block_type, BlockType.PARAGRAPH)

    def test_quote_block(self):
        block = BlockNode("> line1\n> line2")
        html = block.to_html_node().to_html()
        self.assertEqual(block.block_type, BlockType.QUOTE)
        self.assertEqual(html, "<blockquote>line1\nline2</blockquote>")

    def test_quote_block_with_fancies(self):
        block = BlockNode("> **line1**\n> _line2_")
        html = block.to_html_node().to_html()
        self.assertEqual(block.block_type, BlockType.QUOTE)
        self.assertEqual(html, "<blockquote><b>line1</b>\n<i>line2</i></blockquote>")

    def test_quote_block_invalid(self):
        block = BlockNode("> valid\nnot a quote")
        self.assertEqual(block.block_type, BlockType.PARAGRAPH)

    def test_heading1_block(self):
        block = BlockNode("# BREAKING NEWS!")
        html = block.to_html_node().to_html()
        self.assertEqual(block.block_type, BlockType.HEADING)
        self.assertEqual(html, "<h1>BREAKING NEWS!</h1>")

    def test_heading3_block(self):
        block = BlockNode("### Header")
        html = block.to_html_node().to_html()
        self.assertEqual(block.block_type, BlockType.HEADING)
        self.assertEqual(html, "<h3>Header</h3>")

    def test_code_block(self):
        block = BlockNode("```\nprint('hi')\n```")
        html = block.to_html_node().to_html()
        self.assertEqual(block.block_type, BlockType.CODE)
        self.assertEqual(html, "<pre><code>print('hi')\n</code></pre>")

    def test_code_block_with_bold(self):
        block = BlockNode(
            "```This is another very **bold** text that shouldn't change```"
        )
        html = block.to_html_node().to_html()
        self.assertEqual(block.block_type, BlockType.CODE)
        self.assertEqual(
            html,
            "<pre><code>This is another very **bold** text that shouldn't change</code></pre>",
        )

    def test_paragraph_fallback(self):
        block = BlockNode("This is just a normal paragraph.")
        html = block.to_html_node().to_html()
        self.assertEqual(block.block_type, BlockType.PARAGRAPH)
        self.assertEqual(html, "<p>This is just a normal paragraph.</p>")

    def test_paragraph_with_bold(self):
        block = BlockNode("This is a very **bold** message")
        html = block.to_html_node().to_html()
        self.assertEqual(html, "<p>This is a very <b>bold</b> message</p>")


if __name__ == "__main__":
    unittest.main()
