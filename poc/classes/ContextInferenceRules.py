from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxOutlines import AuxOutlines
from poc.classes.RulesOfInferenceBlock import RulesOfInferenceBlock


class ContextInferenceRules:
    @staticmethod
    def start(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        i.context.push_context(AuxOutlines.inferenceRules, i.get_debug_parsing_info(parsing_info))
        i.parse_list.append(parsing_info)

    @staticmethod
    def stop(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        i.context.pop_context([AuxOutlines.inferenceRules], i.get_debug_parsing_info(parsing_info))
        inference_info = RulesOfInferenceBlock(i.parse_list, parsing_info)
        i.parse_list.append(inference_info)
