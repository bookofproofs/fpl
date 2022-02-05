from anytree import AnyNode
from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTPredicate(AuxST):

    def __init__(self, outline: str, i):
        super().__init__(outline, i)
        self._is_asserted = False
        self._is_revoked = False
        if outline == AuxSymbolTable.ids:
            self.zto = i.last_positions_by_rule['Identifier'].pos_to_str()
            self.zfrom = i.corrected_position('Identifier')
        elif outline == AuxSymbolTable.predicate_all:
            self.zto = i.last_positions_by_rule['All'].pos_to_str()
            self.zfrom = i.corrected_position('all')
        elif outline == AuxSymbolTable.intrinsic:
            # intrinsic predicates have no position
            self.zto = ''
            self.zfrom = ''
        elif outline == AuxSymbolTable.extDigit:
            self.zto = i.last_positions_by_rule['extDigit'].pos_to_str()
            self.zfrom = i.corrected_position('extDigit')
        elif outline == AuxSymbolTable.predicate_conjunction:
            self.zto = i.last_positions_by_rule['Conjunction'].pos_to_str()
            self.zfrom = i.corrected_position('and')
        elif outline == AuxSymbolTable.pre:
            self.zto = i.last_positions_by_rule['PremiseBlock'].pos_to_str()
            self.zfrom = i.corrected_position('PremiseHeader')
        elif outline == AuxSymbolTable.con:
            self.zto = i.last_positions_by_rule['ConclusionBlock'].pos_to_str()
            self.zfrom = i.corrected_position('ConclusionHeader')
        elif outline == AuxSymbolTable.predicate_true:
            self.zto = i.last_positions_by_rule['true'].pos_to_str()
            self.zfrom = i.corrected_position('true')
        elif outline == AuxSymbolTable.predicate_false:
            self.zto = i.last_positions_by_rule['false'].pos_to_str()
            self.zfrom = i.corrected_position('false')
        elif outline == AuxSymbolTable.predicate_negation:
            self.zto = i.last_positions_by_rule['Negation'].pos_to_str()
            self.zfrom = i.corrected_position('not')
        elif outline == AuxSymbolTable.predicate_implication:
            self.zto = i.last_positions_by_rule['Implication'].pos_to_str()
            self.zfrom = i.corrected_position('impl')
        elif outline == AuxSymbolTable.predicate_exclusiveOr:
            self.zto = i.last_positions_by_rule['ExclusiveOr'].pos_to_str()
            self.zfrom = i.corrected_position('xor')
        elif outline == AuxSymbolTable.predicate_exists:
            self.zto = i.last_positions_by_rule['Exists'].pos_to_str()
            self.zfrom = i.corrected_position('ex')
        elif outline == AuxSymbolTable.predicate_equivalence:
            self.zto = i.last_positions_by_rule['Equivalence'].pos_to_str()
            self.zfrom = i.corrected_position('iif')
        elif outline == AuxSymbolTable.undefined:
            self.zto = i.last_positions_by_rule['UndefinedHeader'].pos_to_str()
            self.zfrom = i.corrected_position('UndefinedHeader')
        elif outline == AuxSymbolTable.predicate_disjunction:
            self.zto = i.last_positions_by_rule['Disjunction'].pos_to_str()
            self.zfrom = i.corrected_position('or')
        elif outline == AuxSymbolTable.variadic_var:
            self.zto = i.last_positions_by_rule['KeysOfVariadicVariable'].pos_to_str()
            self.zfrom = i.corrected_position('Variable')
        elif outline == AuxSymbolTable.index_value:
            self.zto = i.last_positions_by_rule['IndexValue'].pos_to_str()
            self.zfrom = i.corrected_position('Variable')
        elif outline == AuxSymbolTable.preReferenced:
            self.zto = i.last_positions_by_rule['PremiseHeader'].pos_to_str()
            self.zfrom = i.corrected_position('PremiseHeader')
        elif outline == AuxSymbolTable.digit:
            self.zto = i.last_positions_by_rule['Digit'].pos_to_str()
            self.zfrom = i.corrected_position('Digit')
        else:
            raise NotImplementedError(outline)

    def set_id(self, identifier: str):
        self.id = identifier  # noqa

    def assert_predicate(self):
        self._is_asserted = True

    def revoke_predicate(self):
        self._is_asserted = False
        self._is_revoked = True

    def register_reference(self, reference: AnyNode):
        self.reference = reference  # noqa

    def evaluate(self):
        if self._is_asserted:
            return True
        elif self._is_revoked:
            return False
        else:
            if self.outline == AuxSymbolTable.predicate_true:
                return True
            elif self.outline == AuxSymbolTable.predicate_false:
                return False
            elif self.outline == AuxSymbolTable.predicate_negation:
                return not self.children[0].evaluate()
            elif self.outline == AuxSymbolTable.predicate_conjunction:
                ret = True
                for child in self.children:
                    ret = ret and child.evaluate()
                    if not ret:
                        break
                return ret
            elif self.outline == AuxSymbolTable.predicate_disjunction:
                ret = False
                for child in self.children:
                    ret = ret or child.evaluate()
                    if ret:
                        break
                return ret
            elif self.outline == AuxSymbolTable.predicate_equivalence:
                p = self.children[0].evaluate()
                q = self.children[1].evaluate()
                return p == q
            elif self.outline == AuxSymbolTable.predicate_exclusiveOr:
                p = self.children[0].evaluate()
                q = self.children[1].evaluate()
                return (p and not q) or (q and not p)
            elif self.outline == AuxSymbolTable.predicate_implication:
                p = self.children[0].evaluate()
                q = self.children[1].evaluate()
                return not p or q
            else:
                raise NotImplementedError(self.outline)

    def clone(self):
        return self._copy(AuxSTPredicate(self.outline, self._i))
