

def markdown_to_blocks(markdown):
    linelist = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        block = block.strip()
        if len(block) == 0:
            continue
        linelist.append(block)
    return linelist
