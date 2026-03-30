import unittest
from enum import Enum
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType
from markdown_blocks import markdown_to_html_node, block_to_html_node, text_to_children
from markdown_blocks import paragraph_to_html_node, heading_to_html_node, code_to_html_node
from markdown_blocks import quote_to_html_node, ulist_to_html_node, olist_to_html_node

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_multiline(self):
        block = "```\nthis is code multi line\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_unordered(self):
        block = "- first\n- second\n- third"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)

    def test_block_ordered(self):
        block = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)


    def test_paragraphs(self):
        md = """
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
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

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = "##### this is a heading test"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h5>this is a heading test</h5></div>")

    def test_blockquote(self):
        md = "> this is blockquote"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>this is blockquote</blockquote></div>")

    def test_ulist(self):
        md = "- item one\n- item two\n- item three"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>item one</li><li>item two</li><li>item three</li></ul></div>")
    
    def test_olist(self):
        md = "1. item one\n2. item two\n3. item three"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>item one</li><li>item two</li><li>item three</li></ol></div>")