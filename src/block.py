import re
from enum import Enum
from htmlnode import *
from textnode import *


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

def type_to_tag(block_type,block):
    match block_type:
        case BlockType.HEADING:
            matchhead = re.match(r"^(#{1,6})\s+.+$", block)
            lenhead = len(matchhead.group(1))
            return f"h{lenhead}"
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.UNORDERED_LIST:
            return "ul"
        case BlockType.ORDERED_LIST:
            return "ol"
        case BlockType.CODE:
            return "pre"
        case BlockType.PARAGRAPH:
            return "p"

def text_to_children(text):
    chillist = []
    textl = text_to_textnodes(text)
    for textn in textl:
        chillist.append(text_node_to_html_node(textn))
    return chillist

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    childrens = []

    for block in blocks:
        btype = block_to_block_type(block)
        tag = type_to_tag(btype, block)
        bnode = ParentNode(tag, [])

        lines = block.split("\n")

        match btype:
            case BlockType.HEADING:
                content = re.sub(r"^#{1,6}\s+", "", block, count=1)
                bnode.children.extend(text_to_children(content))

            case BlockType.QUOTE:
                stripped_lines = [re.sub(r"^>\s?", "", line) for line in lines]
                content = " ".join(stripped_lines)
                bnode.children.extend(text_to_children(content))

            case BlockType.UNORDERED_LIST:
                li_nodes = []
                for line in lines:
                    item_text = re.sub(r"^-\s+", "", line, count=1)
                    li_nodes.append(ParentNode("li", text_to_children(item_text)))
                bnode.children.extend(li_nodes)

            case BlockType.ORDERED_LIST:
                li_nodes = []
                for line in lines:
                    item_text = re.sub(r"^\d+\.\s+", "", line, count=1)
                    li_nodes.append(ParentNode("li", text_to_children(item_text)))
                bnode.children.extend(li_nodes)

            case BlockType.CODE:
                code_lines = lines[1:-1]
                code_text = "\n".join(code_lines)
                if block.endswith("\n```"):
                    code_text += "\n"

                code_node = text_node_to_html_node(TextNode(code_text, TextType.CODE))
                bnode.children.append(code_node)

            case BlockType.PARAGRAPH:
                content = " ".join(line.strip() for line in lines)
                bnode.children.extend(text_to_children(content))

        childrens.append(bnode)

    return ParentNode("div", childrens)
