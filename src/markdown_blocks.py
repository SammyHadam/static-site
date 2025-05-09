from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

headings = ["# ", "## ", "### ", "#### ", "##### ", "###### "]
def block_to_block_type(block):
    for heading in headings:
        if block.startswith(heading):
            return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    for line in block.split("\n"):
        if not line.startswith('>'):
            break               
    else:
        return BlockType.QUOTE
    for line in block.split("\n"):
        if not line.startswith('- '):
            break               
    else:
        return BlockType.UNORDERED_LIST
    for index, line in enumerate(block.split("\n")):
        if not line.startswith(f'{index+1}. '):
            break
    else:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

