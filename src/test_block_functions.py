
import unittest
from block_functions import *

markdown = """
# Heading 1

    This is a paragraph of text.

This is another paragraph.

# Another Heading

Now a list:

- Item 1
- Item 2
- Item 3
"""

class TestMarkdownToBlocks(unittest.TestCase):
    def test_length(self):
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 6)

    def test_whitspace_strip(self):
        blocks = markdown_to_blocks(markdown)
        for block in blocks:
            self.assertFalse(block.startswith(" ") or block.endswith(" ") or 
                             block.startswith("\n") or block.endswith("\n"))

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
