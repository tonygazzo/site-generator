import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import *
from inline_functions import *

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, 'This is a bold node')

    def test_italic(self):
        node = TextNode("This is italic", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, "This is italic")

    def test_code(self):
        node = TextNode("This is code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, "This is code")

    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, url="http://www.google.com")
        html_node = text_node_to_html_node(node);
        self.assertEqual(html_node.tag, 'a')
        expected_props = {'href': 'http://www.google.com'}
        self.assertEqual(html_node.props, expected_props)

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, url="http://my.image.url")
        html_node = text_node_to_html_node(node);
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, "")
        expected_props = {'src': 'http://my.image.url', 'alt': 'This is an image'}
        self.assertEqual(html_node.props, expected_props)

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_result = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_result)

    def test_node_skip(self):
        node1 = TextNode("Ignore this", text_type=TextType.BOLD)
        node2= TextNode("This is text with a `code block` word", TextType.TEXT)
        node3 = TextNode("Ignore this too", text_type=TextType.LINK, url='import.url')
        node4 = TextNode("This is a text with some **bold** text", TextType.BOLD)
        starting_nodes = [node1, node2, node3, node4]
        new_nodes = split_nodes_delimiter(starting_nodes, '`', TextType.CODE)
        split_code_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        expected_result = [node1] + split_code_nodes + [node3, node4]
        self.assertEqual(new_nodes, expected_result)
        
    def test_node_skip_2(self):
        node1 = TextNode("Ignore this", text_type=TextType.BOLD)
        node2= TextNode("This is text with a `code block` word", TextType.TEXT)
        node3 = TextNode("Ignore this too", text_type=TextType.LINK, url='import.url')
        node4 = TextNode("This is text with some **bold** text", TextType.TEXT)
        starting_nodes = [node1, node2, node3, node4]
        new_nodes = split_nodes_delimiter(starting_nodes, '**', TextType.BOLD)
        split_code_nodes = [
            TextNode("This is text with some ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        expected_result = [node1, node2, node3] + split_code_nodes
        self.assertEqual(new_nodes, expected_result)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This text has a [link text](www.google.com) link in it"
        )
        self.assertListEqual([("link text", "www.google.com")], matches)

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
        node = TextNode("This text has [link1](www.google.com) and another [link2](www.wikipedia.org)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This text has ", TextType.TEXT),
                TextNode("link1", TextType.LINK, url="www.google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link2", TextType.LINK, url="www.wikipedia.org")
            ],
            new_nodes
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        expected_result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(
            expected_result, result
        )



