import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    linelist = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        block = block.strip()
        if len(block) == 0:
            continue
        linelist.append(block)
    return linelist

def block_to_block_type(block):
    lines = block.split("\n")
    
    if re.match(r"^#{1,6} .+", block):
        return BlockType.HEADING
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    if lines and all(re.match(r"^> ?.*$", line) for line in lines):
        return BlockType.QUOTE
    if lines and all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    is_ordered = True
    for i, line in enumerate(lines, start=1):
        m = re.match(r"^(\d+)\. .+$", line)
        if not m or int(m.group(1)) != i:
            is_ordered = False
            break
    if lines and is_ordered:
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

