import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("p", "Google", None, {"href": "http://www.google.com"})
        result = ' href="http://www.google.com"'
        self.assertEqual(node.props_to_html(), result)

    def test_props_is_none(self):
        node = HTMLNode("p", "Google", None, None)
        result = ""
        self.assertEqual(node.props_to_html(), result)

    def test_repr(self):
        node = HTMLNode("p", "Google", None, None)
        result = "HTMLNode(p, Google, None, None)"
        self.assertEqual(node.__repr__(), result)

    def test_constructor(self):
        node = HTMLNode("p", "Google", None, {"href": "http://www.google.com"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Google")
        self.assertIsNone(node.children)
        self.assertEqual(node.props, {"href": "http://www.google.com"})

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_props(self):
        node = LeafNode("p", "Google", {"href": "http://www.google.com"})
        result = '<p href="http://www.google.com">Google</p>'
        self.assertEqual(node.to_html(), result)

    def test_leaf_tag(self):
        node = LeafNode("a", "Google", {"href": "http://www.google.com"})
        result = '<a href="http://www.google.com">Google</a>'
        self.assertEqual(node.to_html(), result)
    
    def test_tag_none(self):
        node = LeafNode(None, "Google", None)
        result = "Google"
        self.assertEqual(node.to_html(), result)

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
        node = ParentNode("p", [
            LeafNode("b", "Bold"),
            LeafNode(None, " plain "),
            LeafNode("i", "Italic"),
        ])
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold</b> plain <i>Italic</i></p>"
        )  

    def test_to_html_without_tag_raises(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode(None, "text")]).to_html()

    def test_to_html_without_children_raises(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()

    def test_to_html_with_props(self):
        node = ParentNode(
            "div",
            [LeafNode(None, "hello")],
            {"class": "box", "id": "main"}
        )
        self.assertEqual(
            node.to_html(),
            '<div class="box" id="main">hello</div>'
        )

    def test_to_html_deeply_nested(self):
        node = ParentNode("div", [
            ParentNode("section", [
                ParentNode("p", [
                    LeafNode(None, "hello")
                ])
            ])
        ])
        self.assertEqual(
            node.to_html(),
            "<div><section><p>hello</p></section></div>"
        )