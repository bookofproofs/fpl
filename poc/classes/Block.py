class Block:
    outer_block = None
    type = None
    identifiers = set()

    def __init__(self, block_type, outer_block):
        if not type(block_type) is str:
            raise TypeError("block_type must be a string, was " + str(block_type))
        if not type(outer_block) is Block:
            raise TypeError("outer_block must be a Block, was " + str(outer_block))
        self.outer_block = outer_block
        self.type = block_type

    '''
    Register a new identifier in the scope of this Block.
    If the identifier already exists in the block or in any of the outer_blocks, an error is raised. 
    Search for an identifier in the scope of self and all outer_blocks
    and add the identifier return the type of the outer_bloc, otherwise
    '''

    def register_identifier(self, identifier):
        if not type(identifier) is str:
            raise TypeError("identifier must be a string, was " + str(identifier))
        scope = self.get_scope_where_registered(identifier)
        if scope is not None:
            raise ReferenceError("identifier [" + identifier + "] already registered the scope of [" + scope + "]")
        else:
            self.identifiers.add(identifier)

    '''
    Search for an identifier in the scope of this Block and all outer_blocks
    and return either the type of the block, in which the identifier was found or None
    '''

    def get_scope_where_registered(self, identifier):
        if identifier in self.identifiers:
            return self.type
        elif self.outer_block is not None:
            return self.outer_block.get_scope_where_registered(identifier)
        else:
            return None
