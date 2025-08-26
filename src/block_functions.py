import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    QUOTE = "quote"
    CODE = "code"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [x.strip() for x in blocks]
    return blocks

def block_to_block_type(block):
    if re.match(r"\#{1,6} ", block):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        lines = block.split("\n")
        is_quote = True
        for line in lines:
            if not line.startswith(">"):
                is_quote = False
                break
        if is_quote:
            return BlockType.QUOTE


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

# markdown_to_blocks(markdown)
# block_to_block_type("### Heading")
# block_to_block_type("######## Heading")
block_to_block_type("```some code```")

