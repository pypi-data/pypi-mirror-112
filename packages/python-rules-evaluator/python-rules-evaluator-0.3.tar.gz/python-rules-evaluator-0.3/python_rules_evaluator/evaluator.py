import re
import traceback
from os.path import join
from pathlib import Path
from pprint import pprint
from sys import stdout
from typing import Union
import json

import yaml
from friendlylog import colored_logger as log

from python_rules_evaluator.modules.jsongeek import dotpath_get_value


class Evaluator():
    RE_VAR = r"\$([^ '\"\), ]+)"

    def __init__(self, rules_file: str, functions: dict = {}):
        self.rules_file = rules_file
        self.functions = functions
        with open(join(str(Path().absolute()), rules_file)) as rules_file:
            self.rules = yaml.load(rules_file, Loader=yaml.FullLoader)

    def __replace_functions(self, expr: str, context: dict):
        for match in re.finditer(r"\@([^\(]+)\(", expr):
            if match:
                func = re.sub(r'\@', '', match.group(1))
                arg_match = re.search(
                    f"{func}\\((?<!')([^\\)]+)(?!')\\)", expr, flags=re.MULTILINE)
                args = {}
                if arg_match:
                    arg_str = arg_match.group(1).strip()
                    args = eval(f"dict({arg_str})")

                if func in self.functions:
                    result = self.functions[func](**args)
                    expr = re.sub(
                        f'\\\\@{func}\\([^\\)]+\\)', str(result), expr, 1)
                else:
                    log.warning(f"Function '{func}' is not defined.")
        return expr

    def __replace_vars(self, expr: str, context: dict, informative=False):
        for match in re.finditer(self.RE_VAR, expr):
            if match:
                var = re.sub(r'\$', '', match.group(0))
                if var in context['vars']:
                    expr = re.sub(
                        f"\\${var}", f"{context['vars'][var]}{' (' + var + ')' if informative else ''}", expr)
                elif var in context['consts']:
                    expr = re.sub(
                        f"\\${var}", f"{context['consts'][var]}{' (' + var + ')' if informative else ''}", expr)
                elif 'fields' in context and dotpath_get_value(context['fields'], var) is not None:
                    expr = re.sub(
                        f"\\${var}", f"{dotpath_get_value(context['fields'], var)}{' (' + var + ')' if informative else ''}", expr)
                else:
                    log.warning(f"'{var}' is not defined.")
                    expr = re.sub(f"\\${var}", 'None', expr)
        return expr

    def __exec_function(self, body: str, context: dict):
        imports = [
            "from python_rules_evaluator.modules.functions import get_max, get_min"
        ]
        body_lines = []
        for line in body.split("\n"):
            if len(line.strip()) > 0:
                line = self.__replace_vars(line, context)
                line = self.__replace_functions(line, context)
                body_lines.append(line)
        lines = ''.join(map(lambda imp: f"\n\t{imp}", imports))
        lines += ''.join(map(lambda line: f"\n\t{line}", body_lines))

        funcs = {}
        exec(f"def func(): {lines}", self.functions, funcs)

        return funcs['func']()

    def __eval_and_or(self, condition: Union[dict, list, str], context: dict):
        evaluation = ''
        if isinstance(condition, list):
            for cond in condition:
                evaluation += f"{self.__eval_and_or(cond, context)}"
        elif isinstance(condition, dict):
            evaluation = ''
            # default is and
            if 'or' in condition:
                op = 'or'
            elif 'and' in condition:
                op = 'and'
            else:
                op = None
            if op:
                for idx, cond in enumerate(condition[op]):
                    if idx == 0:
                        evaluation += '('
                    evaluation += f" {self.__eval_and_or(cond, context)} "
                    if idx == len(condition[op]) - 1:
                        evaluation += ')'
                    else:
                        evaluation += f" {op} "
                # print(evaluation)
                # print(self.__replace_vars(evaluation, context))
                # print(self.__replace_functions(evaluation, context))
            else:
                raise(Exception("Only 'and' and 'or' are allowed operators.", condition))
        else:
            return f"( {condition} )"
        return self.__eval_condition(evaluation, context)

    def __eval_condition(self, condition: Union[bool, str, list], context: dict):
        """
        A condition is always True or False
        """
        if isinstance(condition, bool):
            return condition
        if isinstance(condition, str):
            condition = self.__replace_vars(condition, context)
            condition = self.__replace_functions(condition, context)
            result = False
            try:
                result = eval(condition)
            except Exception as ex:
                log.waring(ex)
            finally:
                return result
        elif isinstance(condition, list):
            return self.__eval_and_or(condition, context)

    def __evaluate_variables(self, _vars: dict, obj: dict, context: dict):
        vars = context['vars']
        for var, fieldpath in _vars.items():
            if (isinstance(fieldpath, str)):
                vars[var] = dotpath_get_value(obj, fieldpath)
            if (isinstance(fieldpath, dict)):
                if 'func' in _vars[var]:
                    vars[var] = self.__exec_function(
                        _vars[var]['func'], context)
                elif 'cond' in _vars[var]:
                    vars[var] = self.__eval_condition(
                        _vars[var]['cond'], context)
            # log.debug(f"Variable: {var}={vars[var]}")

    def __evaluate_field(self, field_name, field_spec, obj, context):
        ret = {}
        for action in field_spec.keys():
            new_field = None
            if action.startswith('cond.'):
                [_, new_field] = action.split('.')
                ret[new_field] = self.__eval_condition(
                    field_spec[action], context)
            elif action.startswith('func.'):
                [_, new_field] = action.split('.')
                ret[new_field] = self.__exec_function(
                    field_spec[action], context)
            if new_field is not None:
                if new_field == 'self':
                    ret = ret[new_field]
            context['fields'][field_name] = ret
        return ret

    def __do_evaluate(self, block: list, obj: dict, result: Union[dict, list] = {}, context: dict = {'consts': {}, 'vars': {}, 'fields': {}}):
        # go through the list of blocks (treated in order of occurrence)
        for op in block:
            # if its a consts operation
            if 'consts' in op:
                context['consts'].update(op['consts'])
            # if its a vars operation
            if 'vars' in op:
                self.__evaluate_variables(op['vars'], obj, context)
            # if its a fields operation
            if 'fields' in op:
                for field in op['fields'].keys():
                    # print('field', op['fields'][field])
                    result[field] = self.__evaluate_field(
                        field, op['fields'][field], obj, context)
                    if isinstance(result[field], dict):
                        result[field].update(
                            {'evaluation': self.__get_evaluation(op['fields'][field], context)})

            # if its a for operation
            if 'for' in op:
                block = op['for']
                if 'field' not in block:
                    raise(Exception("'field' is required in 'for'.", block))
                if 'as' not in block:
                    raise(Exception("'as' is required in 'for'.", block))
                if 'evaluate' not in block:
                    raise(Exception("'evaluate' is required in 'for'.", block))
                for idx, item in enumerate(dotpath_get_value(obj, block['field'])):
                    context['vars'].update({
                        '__field__': block['field'],
                        '__idx__': idx,
                        '__as__': block['as']
                    })
                    if block['field'] not in result:
                        result[block['field']] = []
                    result[block['field']].append({})
                    self.__do_evaluate(
                        block['evaluate'], item, result[block['field']][idx], context)
        return result

    @ staticmethod
    def __debug_log_dict(text: str, dct: dict):
        log.debug(f"--{text}--")
        for key, val in dct.items():
            log.debug(f"{key}: {val}")

    def __get_evaluation(self, evaluation, context):
        return json.loads(self.__replace_vars(
            json.dumps(evaluation), context, informative=True))

    def __get_field(self, item: Union[dict, list], field, found={}, keys=[]):
        if isinstance(item, list):
            for i in item:
                self.__get_field(i, field, found)
        if isinstance(item, dict):
            for key in item.keys():
                if key == 'for':
                    found.update({item[key]['field']: []})
                    keys.append(item[key]['field'])
                if key == field:
                    found.update(item[key])
                else:
                    # print('next', item[key])
                    self.__get_field(item[key], field, found)
        return found

    def evaluate(self, obj: Union[dict, list]):
        try:
            context = {'consts': {}, 'vars': {}, 'fields': {}}
            result = self.__do_evaluate(
                self.rules, obj, result={}, context=context)

            return result

        except Exception as ex:
            rules_file = re.sub(r".*\/", "", self.rules_file)
            # pp(ex)
            log.error(f"{rules_file}: {ex}")
            traceback.print_exc(file=stdout)
