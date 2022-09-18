from poc.classes.AuxST import AuxSTOutline
from poc.classes.AuxSTVarDec import AuxSTVarDec
from poc.fplerror import FplVariableDuplicateInVariableList
from poc.fplerror import FplTemplateMisused


class AuxSymbolTableHelpers:

    @staticmethod
    def add_vars_to_node(i, parent: AuxSTOutline, named_var_declaration):
        distinct_vars = dict()
        ast_info = named_var_declaration.get_ast_info()
        if named_var_declaration.var_list is not None:
            for var in reversed(named_var_declaration.var_list):
                if var.var.id.startswith("tpl"):
                    named_var_declaration.get_error_mgr().add_error(
                        FplTemplateMisused(var.var.id, var.var.zfrom, ast_info.file)
                    )
                if var.var.id in distinct_vars:
                    named_var_declaration.get_error_mgr().add_error(
                        FplVariableDuplicateInVariableList(distinct_vars[var.var.id], var.var,
                                                           ast_info.file))
                else:
                    distinct_vars[var.var.id] = var.var
                var_dec = AuxSTVarDec(i)
                var_dec.zto = named_var_declaration.zto
                var_dec.zfrom = var.var.zfrom
                var_dec.id = var.var.id
                var_dec.parent = parent
                cloned_type = named_var_declaration.var_type.generalType.clone()
                cloned_type.parent = var_dec
