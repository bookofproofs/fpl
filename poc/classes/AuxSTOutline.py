from anytree import AnyNode, Walker
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTOutline(AnyNode):
    """
    A class for elements of the symbol table that have an outline
    """

    def __init__(self, parent: AnyNode, outline: str):
        super().__init__()
        self.outline = outline
        self.parent = parent
        self._long_id = None
        self._scope = None
        self._minor_scope = None
        self._copied_path = tuple()

    def get_long_id(self):
        raise NotImplementedError(str(type(self)))

    def get_scope(self):
        """
        Returns the Scope node of self according to the symbol table.
        The Scope equals the most outer FPL building block containing self in the symbol table.
        :return: Scope of self
        """
        if self._scope is None:
            if len(self.path) > 3:
                self._scope = self.path[3]
            elif len(self._copied_path) > 3:
                self._scope = self._copied_path[3]
            else:
                raise NotImplementedError()
        return self._scope

    def get_copied_path(self):
        return self._copied_path

    def get_minor_scope(self):
        """
        Returns the Minor Scope node of a self according to the symbol table.
        The Minor Scope equals the most inner FPL building block containing self in the symbol table.
        According to the FPL syntax, the Minor Scope might equal the Scope node unless
        the self node resists inside an FPL Property of the Scope node.
        :return: Minor Scope of self
        """
        if self._minor_scope is None:
            # We use the anytree.Walker to determine if between the scope node and self there is an FPL property.
            # If there is, we set the minor scope of self to this property, otherwise to the scope node itself.
            w = Walker()
            scope = self.get_scope()
            upwards, common, downwards = w.walk(scope, self)
            if len(downwards) > 0 and downwards[0].outline == AuxSTConstants.properties:
                # return the property node being on the path from the scope node to the self node
                self._minor_scope = downwards[1]
            else:
                # there is no property node between, just fall back to the scope node
                self._minor_scope = scope
        return self._minor_scope

    def evaluate(self, sem):
        raise NotImplementedError(str(sem.eval_stack[-1].node))
