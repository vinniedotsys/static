import unittest

from htmlnode import HtmlNode, LeafNode

class TestHtmlNode(unittest.TestCase):
    def test_child(self):
        node = HtmlNode("body", None, "h1")
        print(node)

    def test_value(self):
        node = HtmlNode("h1", "This is the top of the page")
        print(node)

    def test_attributes(self):
        node = HtmlNode("a",
            "Google",
             None,
            {
        "href": "https://www.google.com",
        "target": "_blank",
            })
        print(node)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_link(self):
        node = LeafNode(
            "a",
            "Clique !",
            {
                "href": "https://www.google.com",
                "target": "_blank",
            })
        self.assertEqual(node.to_html(), '<a href="https://www.google.com" target="_blank">Clique !</a>')


if __name__ == "__main__":
    unittest.main()
