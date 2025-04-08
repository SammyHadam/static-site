from textnode import TextNode, TextType

def main():
    # Create an instance of TextNode
    node = TextNode("This is some anchor text", TextType.BOLD, "https://www.boot.dev")
    # Print the node
    print(node)

if __name__ == "__main__":
    main()