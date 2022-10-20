from poc.fplerror import FplTypeMismatch
from poc.classes.AuxEvaluationRegister import AuxEvaluationRegister


class EvaluateParams:

    @staticmethod
    def evaluate_recursion(sem, node, expected_type=None, building_block=None, instance_guid=None):
        """

        :param sem:
        :param node:
        :param expected_type:
        :param building_block:
        :param instance_guid:
        :return:
        """
        # create a new evaluation params set
        register = AuxEvaluationRegister(node, expected_type)

        if building_block is None:
            EvaluateParams._propagate(sem, register)
        else:
            EvaluateParams._create(register, building_block, instance_guid)

        if EvaluateParams._evaluation_necessary(register):
            register = EvaluateParams._re_evaluate(sem, node, register, expected_type)
        return register

    @staticmethod
    def _propagate(sem, register):
        # propagate the last building block, its guid, a list of argument types and if we want to check these args
        previous = sem.eval_stack[-1]
        register.building_block = previous.building_block
        register.instance_guid = previous.instance_guid
        register.instance = previous.instance

    @staticmethod
    def _create(register, building_block, instance_guid):
        register.building_block = building_block
        register.instance_guid = instance_guid
        register.instance = building_block.get_instance(instance_guid)

    @staticmethod
    def _evaluation_necessary(register):
        register_id = register.node.get_long_id()
        if register.instance.has_register(register_id):
            EvaluateParams._copy_evaluation(register_id, register)
            return register.is_dirty  # evaluation is necessary, if the register exists but is dirty
        # evaluation is necessary, if the register does not exist
        return True

    @staticmethod
    def _copy_evaluation(source_register_id, target_register):
        register = target_register.instance.get_register(source_register_id)
        target_register.value = register.value
        target_register.evaluation_error = register.evaluation_error
        target_register.argument_error = register.argument_error
        target_register.is_dirty = register.is_dirty

    @staticmethod
    def _re_evaluate(sem, node, register, expected_type):
        # push it on the stack
        sem.eval_stack.append(register)

        node.evaluate(sem)  # start recursion
        register = sem.eval_stack.pop()  # garbage-collect the stack

        if expected_type is not None:
            # store the last value that we can retrieve by some recursive caller to skip nodes that have
            # no expected type (and whose value is None)
            sem.last_value = register.value

        # check if there is a type mismatch
        if register.expected_type is not None:
            if not register.expected_type.accepts(register.value.get_declared_type()):
                sem.error_mgr.add_error(
                    FplTypeMismatch(node, register.expected_type.id, register.value.get_declared_type().id)
                )
                register.evaluation_error = True
            # store the value of eval_params of the node in the instance of the building block
            register.instance.set_register(register.node.get_long_id(), register)
        return register
