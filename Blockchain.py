from Block import Block

class Blockchain:
    def __init__(self):
        self.blocks = [Block.genesis()]

    def add_block(self, block):
        self.blocks.append(block)

    def to_json(self):
        data = {}
        json_blocks = []

        for block in self.blocks:
            json_blocks.append(block.to_json())

        data['blocks'] = json_blocks
        return data