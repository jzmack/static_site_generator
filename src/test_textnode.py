import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.PLAIN)
        self.assertNotEqual(node, node2)
    
    def test_not_eq2(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        node2 = TextNode("This is a text node2", TextType.PLAIN)
        self.assertNotEqual(node, node2)
    
    def test_not_eq3(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("This is a link", TextType.LINK, "https://example.com")
        self.assertEqual(node.url, "https://example.com")
        self.assertIsNone(TextNode("No URL", TextType.PLAIN).url)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(repr(node), "TextNode('This is a text node', 'bold', None)")
        node_with_url = TextNode("Example Link", TextType.LINK, "https://example.com")
        self.assertEqual(repr(node_with_url), "TextNode('Example Link', 'link', 'https://example.com')")

if __name__ == "__main__":
    unittest.main()
