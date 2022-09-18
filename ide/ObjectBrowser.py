import tkinter as tk
from tkinter import ttk
from anytree import AnyNode
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.util.fplutil import Utils


class ObjectBrowser:
    def __init__(self, panedMainWindow, ide):
        self.ide = ide
        self._object_browser_tree = ttk.Treeview(panedMainWindow, selectmode='browse')
        self._object_browser_tree["columns"] = ("Status", "File", "HiddenPos")
        self._object_browser_tree.column("#0", width=395, minwidth=395, stretch=tk.YES, anchor=tk.W)
        self._object_browser_tree.column("Status", width=50, minwidth=50, stretch=tk.YES, anchor=tk.W)
        self._object_browser_tree.column("File", width=100, minwidth=100, stretch=tk.YES, anchor=tk.W)
        self._object_browser_tree.column("HiddenPos", width=0, stretch=tk.NO)
        self._object_browser_tree.heading("#0", text="Theory Structure", anchor=tk.W)
        self._object_browser_tree.heading("Status", text="Status", anchor=tk.W)
        self._object_browser_tree.heading("File", text="File", anchor=tk.W)
        self._object_browser_tree.heading("HiddenPos", text="HiddenPos", anchor=tk.W)
        self._object_browser_tree.bind("<Double-Button-1>", self._select_node)
        panedMainWindow.add(self._object_browser_tree)

    def clear(self):
        self._object_browser_tree.delete(*self._object_browser_tree.get_children())

    def refresh(self, root: AnyNode):
        """
        Updates the object tree according to the current syntax tree.
        :param root: root of the syntax tree
        :return: None
        """
        # dictionary prevents creating multiple theory nodes for the same namespace split across different FPL files
        tree_view_theories = dict()
        # remove all items from previous tree_view
        self._object_browser_tree.delete(*self._object_browser_tree.get_children())
        theories = AuxSymbolTable.get_theories(root)
        for theory_node in theories:
            if theory_node.namespace not in tree_view_theories:
                tree_view_theories[theory_node.namespace] = \
                    self._object_browser_tree.insert('', index=tk.END,
                                                     iid=theory_node.namespace,
                                                     text=theory_node.namespace,
                                                     values=("", "", "0.0"))
            self._propagate_object_tree_children(theory_node, tree_view_theories[theory_node.namespace],
                                                 AuxSTConstants.block_ir_root, "_i", "Inference Rules")
            self._propagate_object_tree_children(theory_node, tree_view_theories[theory_node.namespace],
                                                 AuxSTConstants.block_axiom_root, "_a", "Axioms")
            self._propagate_object_tree_children(theory_node, tree_view_theories[theory_node.namespace],
                                                 AuxSTConstants.block_conj_root, "_c", "Conjectures")
            self._propagate_object_tree_children(theory_node, tree_view_theories[theory_node.namespace],
                                                 AuxSTConstants.block_def_root, "_d", "Definitions")
            self._propagate_object_tree_children(theory_node, tree_view_theories[theory_node.namespace],
                                                 AuxSTConstants.block_thm_root, "_t", "Theorems")
            self._propagate_object_tree_children(theory_node, tree_view_theories[theory_node.namespace],
                                                 AuxSTConstants.block_prop_root, "_p", "Propositions")
            self._propagate_object_tree_children(theory_node, tree_view_theories[theory_node.namespace],
                                                 AuxSTConstants.block_lem_root, "_l", "Lemmas")

    def _propagate_object_tree_children(self, theory_node: AnyNode, treeview_theory_node, outline: str, postfix: str,
                                        node_title: str):
        syntax_tree_node = AuxSymbolTable.get_child_by_outline(theory_node, outline)
        if len(syntax_tree_node.children) > 0:
            tree_view_node = self._object_browser_tree.insert(treeview_theory_node, index=tk.END,
                                                              iid=theory_node.namespace + postfix,
                                                              text=node_title,
                                                              values=("", "", "0.0"))
            need_def_objects = True
            need_def_objects_constructors = True
            need_def_objects_properties = True
            need_def_predicates = True
            need_def_predicate_properties = True
            need_def_functions = True
            need_def_function_properties = True
            ob = None
            pr = None
            fu = None
            for child in syntax_tree_node.children:
                if outline == AuxSTConstants.block_def_root:
                    if child.def_type == AuxSTConstants.classDeclaration:
                        if need_def_objects:
                            ob = self._object_browser_tree.insert(parent=tree_view_node, index=tk.END,
                                                                  iid=theory_node.namespace + postfix + '_o',
                                                                  text='Objects',
                                                                  values=("", "", "0.0"))
                            need_def_objects = False
                        obj = self._object_browser_tree.insert(parent=ob, index=tk.END,
                                                               iid=theory_node.namespace + postfix + '_o' + child.id,
                                                               text=child.id,
                                                               values=("ok", theory_node.file_name, child.zfrom))
                        self.__propagate_object_tree_children_sub(theory_node, child, obj,
                                                                  theory_node.namespace + postfix + '_o' + child.id + '_c',
                                                                  AuxSTConstants.classConstructors,
                                                                  need_def_objects_constructors)
                        self.__propagate_object_tree_children_sub(theory_node, child, obj,
                                                                  theory_node.namespace + postfix + '_o' + child.id + '_p',
                                                                  AuxSTConstants.properties,
                                                                  need_def_objects_properties)
                    elif child.def_type == AuxSTConstants.predicateDeclaration:
                        if need_def_predicates:
                            pr = self._object_browser_tree.insert(parent=tree_view_node, index=tk.END,
                                                                  iid=theory_node.namespace + postfix + '_p',
                                                                  text='Predicates',
                                                                  values=("", "", "0.0"))
                            need_def_predicates = False
                        prop = self._object_browser_tree.insert(parent=pr, index=tk.END,
                                                                iid=theory_node.namespace + postfix + '_p' + child.id,
                                                                text=child.id,
                                                                values=("ok", theory_node.file_name, child.zfrom))
                        self.__propagate_object_tree_children_sub(theory_node, child, prop,
                                                                  theory_node.namespace + postfix + '_p' + child.id + '_p',
                                                                  AuxSTConstants.properties,
                                                                  need_def_predicate_properties)
                    elif child.def_type == AuxSTConstants.functionalTerm:
                        if need_def_functions:
                            fu = self._object_browser_tree.insert(parent=tree_view_node, index=tk.END,
                                                                  iid=theory_node.namespace + postfix + '_f',
                                                                  text='Functions',
                                                                  values=("", "", "0.0"))
                            need_def_functions = False
                        func = self._object_browser_tree.insert(parent=fu, index=tk.END,
                                                                iid=theory_node.namespace + postfix + '_f' + child.id,
                                                                text=child.id,
                                                                values=("ok", theory_node.file_name, child.zfrom))
                        self.__propagate_object_tree_children_sub(theory_node, child, func,
                                                                  theory_node.namespace + postfix + '_f' + child.id + '_p',
                                                                  AuxSTConstants.properties,
                                                                  need_def_function_properties)
                    else:
                        raise NotImplementedError(outline)
                else:
                    self._object_browser_tree.insert(parent=tree_view_node, index=tk.END,
                                                     iid=theory_node.namespace + postfix + child.id, text=child.id,
                                                     values=("ok", theory_node.file_name, child.zfrom))

    def __propagate_object_tree_children_sub(self, theory_node: AnyNode, node: AnyNode, tree_view_node, postfix: str,
                                             outline: str, need_for_outline_node: bool):
        if outline == AuxSTConstants.classConstructors:
            sub_node = AuxSymbolTable.get_child_by_outline(node, AuxSTConstants.classConstructors)
            sub_node_title = 'Constructors'
        else:
            sub_node = AuxSymbolTable.get_child_by_outline(node, AuxSTConstants.properties)
            sub_node_title = 'Properties'

        if len(sub_node.children) > 0:
            if need_for_outline_node:
                sub_node_tree_view = self._object_browser_tree.insert(parent=tree_view_node, index=tk.END,
                                                                      iid=postfix + node.id,
                                                                      text=sub_node_title,
                                                                      values=("", "", "0.0"))
            for sub_sub_node in sub_node.children:
                if sub_sub_node.outline == AuxSTConstants.classDefaultConstructor:
                    self._object_browser_tree.insert(parent=sub_node_tree_view, index=tk.END,
                                                     iid=postfix + node.id + sub_sub_node.id,
                                                     text=sub_sub_node.id + " (intrinsic)",
                                                     values=("", "", "0.0"))
                else:
                    self._object_browser_tree.insert(parent=sub_node_tree_view, index=tk.END,
                                                     iid=postfix + node.id + sub_sub_node.id,
                                                     text=sub_sub_node.id,
                                                     values=("ok", theory_node.file_name, sub_sub_node.zfrom))

    def _select_node(self, event=None):
        record = Utils.identify_clicked_treeview_item(self._object_browser_tree)
        # ignore all '0.0' records or records with empty filename since they are not selectable
        if record[2] != "0.0" and record[1] != "":
            file_name = record[1]
            file_pos = record[2].split('.')
            self.ide.set_position_in_editor(int(file_pos[0]), int(file_pos[1]), file_name)

