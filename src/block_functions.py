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
    if block.startswith("-"):
        lines = block.split("\n")
        is_ul = True
        for line in lines:
            if not line.startswith("-"):
                is_ul = False
                break
        if is_ul:
            return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        lines = block.split("\n")
        is_ol = True
        for i, line in enumerate(lines):
            if not line.startswith(f"{i+1}. "):
                is_ol = False
                break
        if is_ol:
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

markdown = """
# Heading 1

    This is a paragraph of text.

This is another paragraph.

# Another Heading

Now a list:

- Item 1
- Item 2
- Item 3

1. ordered_item 1
2. ordered_item 2
3. ordered_item 3

- Looks like a list
But should be a
- normal paragraph
"""

# markdown_to_blocks(markdown)
# block_to_block_type("### Heading")
# block_to_block_type("######## Heading")
# block_to_block_type("```some code```")
# print(block_to_block_type("- item 1\n- item2\n- item3"))
# print(block_to_block_type("- item 1\nitem2\n- item3"))
# print(block_to_block_type("1. item 1\n2. item2\n3. item3"))
# print(block_to_block_type("1. item 1\n3. item2\n4. item3"))
