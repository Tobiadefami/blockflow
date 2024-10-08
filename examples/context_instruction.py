import glob

from rich import print

from blockflow.block import Block, TextBlock
from blockflow.tokenizer import create_tokenizer

text_files = glob.glob("data/*.txt")
docs = []
for file in text_files:
    doc = open(file).read()
    docs.append(doc)

# We want an even amount of information from each of the documents
context_block = Block(name="context block", boundary="sentence", truncate="right")
instruction_block = Block(text= "never truncate", name="instruction block", truncate = "never")
block = Block(name="overall block", max_tokens = 2048, tokenizer = create_tokenizer(), children=[context_block, instruction_block])

for doc in docs:
    context_block += TextBlock(
        text=doc,
        boundary="sentence",
    )

print(block.rich_text())

# child_block_1 = TextBlock(
#         text="this is a prompt that should be truncated by the truncation value",
#         name="child block 1",
#         tokenizer= create_tokenizer(),
#     )
# child_block_2 = TextBlock(
#     text="this is a sample prompt that should never ever be truncated",
#     name="child block 2",
#     truncate="never",
#     tokenizer= create_tokenizer(),
# )
# parent = Block(
#     name="parent block", tokenizer = create_tokenizer(), children=[child_block_1, child_block_2], max_tokens=12, truncate = "right"
# )

# print(parent.text())
# if truncate == "never" and max_length is < parent block max_length
# instruction_block.text() remains the same for every iteration while context_block.text() changes due to the truncation strategy

# if truncate == "never", and max_length is > than parent block max_length
# return error message, instruction_block should not be truncated and parent block max_length should not be altered

# if parent block has multiple children with truncate=="never", and the aggregate of all children max_tokens exceed parent block max_length:
#   return error message, children block max_length > parent block max_length    

