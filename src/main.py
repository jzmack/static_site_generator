from textnode import TextNode, TextType

def main():

    test_node_plain = TextNode("Hello", TextType.PLAIN)
    test_node_bold = TextNode("Bold text", TextType.BOLD)
    test_node_link = TextNode("Example Link", TextType.LINK, "https://example.com")
    print(test_node_plain)
    print(test_node_bold)
    print(test_node_link)

main()
