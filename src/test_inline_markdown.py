import unittest
import re
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    def test_invalid_markdown(self):
        node = TextNode("This is text with no `closing delimiter", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)
    
    def test_delim_bold_double(self):
        node = TextNode("This is text with a **bolded** word and **another**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual([
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded", TextType.BOLD),
            TextNode(" word and ", TextType.TEXT),
            TextNode("another", TextType.BOLD),
        ], new_nodes)

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual([
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
        ], new_nodes)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdonw_links(self):
        matches = extract_markdown_links("Link [link](http://www.boot.dev)")
        self.assertListEqual([("link", "http://www.boot.dev")], matches)

    def test_no_image(self):
        matches = extract_markdown_images("")
        self.assertListEqual([], matches)

    def test_mixed_1(self):
        matches = extract_markdown_images("Image ![image](http://www.google.com)")
        matches_link = extract_markdown_links("Link ![link](http://www.boot.dev)")
        self.assertListEqual([], matches_link)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with [link](https://www.boot.dev)",
            TextType.TEXT,
            )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )
    
    def test_no_links(self):
        node = TextNode("This is plain text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_mixed_2(self):
        node = TextNode("image ![image](https://www.google.com) link [link](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        new_nodes_link = split_nodes_link(new_nodes)
        self.assertListEqual(
            [
                TextNode("image ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://www.google.com"),
                TextNode(" link ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev")
            ],
            new_nodes_link
        )

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes("some markdown string")
        self.assertListEqual(
            [TextNode("some markdown string", TextType.TEXT)],
            nodes,
        )
    
    def test_mixed_3(self):
        nodes = text_to_textnodes("some markdown **bold** _italic_ `code` image ![image](https://www.google.com) link [link](https://www.boot.dev)")
        self.assertListEqual(
            [
                TextNode("some markdown ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" image ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://www.google.com"),
                TextNode(" link ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev")
            ],
            nodes
        )


if __name__ == "__main__":
    unittest.main()