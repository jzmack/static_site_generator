import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_initialization_defaults(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_initialization_with_values(self):
        node = HTMLNode(tag="div", value="Hello", children=[], props={"class": "greeting"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "greeting"})

    def test_props_to_html(self):
        node = HTMLNode(props={"id": "main", "class": "container"})
        expected = ' id="main" class="container"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_none(self):
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = HTMLNode(tag="p", value="Text", children=None, props={"style": "color:red;"})
        expected = "HTMLNode('p', 'Text', None, {'style': 'color:red;'})"
        self.assertEqual(repr(node), expected)

    def test_to_html_not_implemented(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_with_tag_and_props(self):
        node = LeafNode("span", "Click me", props={"class": "btn", "id": "click"})
        self.assertEqual(node.to_html(), '<span class="btn" id="click">Click me</span>')

    def test_leaf_to_html_without_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_to_html_raises_value_error(self):
        with self.assertRaises(ValueError):
            LeafNode("div", None)

    def test_leaf_repr(self):
        node = LeafNode("b", "Bold", props={"style": "font-weight:bold;"})
        expected = "HTMLNode('b', 'Bold', None, {'style': 'font-weight:bold;'})"
        self.assertEqual(repr(node), expected)

    def test_leaf_props_to_html_none(self):
        node = LeafNode("em", "Italic", props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_leaf_props_to_html_empty_dict(self):
        node = LeafNode("em", "Italic", props={})
        self.assertEqual(node.props_to_html(), "")

class TestParentNode(unittest.TestCase):
    def test_valid_parent_node(self):
        child1 = LeafNode("span", "Hello")
        child2 = LeafNode("span", "World")
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(parent.to_html(), "<div><span>Hello</span><span>World</span></div>")

    def test_parent_node_with_props(self):
        child = LeafNode("em", "Text")
        parent = ParentNode("section", [child], props={"class": "highlight"})
        self.assertEqual(parent.to_html(), '<section class="highlight"><em>Text</em></section>')

    def test_missing_tag_raises_error(self):
        child = LeafNode("p", "Content")
        with self.assertRaises(ValueError) as context:
            ParentNode(None, [child])
        self.assertEqual(str(context.exception), "ParentNode requires a non-None tag.")

    def test_missing_children_raises_error(self):
        with self.assertRaises(ValueError) as context:
            ParentNode("div", None)
        self.assertEqual(str(context.exception), "ParentNode requires a non-None children list.")

    def test_children_not_list_raises_type_error(self):
        child = LeafNode("p", "Text")
        with self.assertRaises(TypeError):
            ParentNode("div", child)  # Not a list

    def test_invalid_child_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            ParentNode("div", ["not a node"])

    def test_child_missing_to_html_method_raises_error(self):
        class FakeNode:
            pass
        with self.assertRaises(TypeError):
            ParentNode("div", [FakeNode()])

    def test_empty_children_list_renders_valid_html(self):
        parent = ParentNode("ul", [])
        self.assertEqual(parent.to_html(), "<ul></ul>")

if __name__ == "__main__":
    unittest.main()

