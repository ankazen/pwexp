import re
import operator
from peewee import ForeignKeyField


P_Rule = re.compile(r'(\w+):([\w.]+)([=>]+)([\w\[\]]+)')
P_Exp = re.compile(r'([\w.]+)([=>]+)([\w\[\]]+)')
P_Exp_Val = re.compile(r'\[(.+)\]')


comparison_operators = {
    "<": operator.lt,
    "<=": operator.le,
    "=": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    ">=": operator.ge
}


def get_obj_attr(qs, model, exp):
    if '.' not in exp:
        col = exp
        exp = None
    else:
        col, exp = exp.split('.')

    result = getattr(model, col)
    if isinstance(result, ForeignKeyField):
        qs = qs.join(result.rel_model)

    if exp:
        qs, result = get_obj_attr(qs, result, exp)
    return qs, result


def get_val(val, context):
    if '[' not in val:
        return val

    mc = P_Exp_Val.match(val)
    if not mc:
        return val

    key = mc.groups()[0]
    val = context[key]
    return val


def filter_exp(qs, exp, context=None):
    mc = P_Exp.match(exp)
    if not mc:
        return qs
    M = qs.model
    col, op, val = mc.groups()
    qs, col = get_obj_attr(qs, M, col)
    val = get_val(val, context)
    _exp = comparison_operators[op](col, val)
    qs = qs.where(_exp)

    return qs


def filter_rule(qs, exp, context=None):
    mc = P_Rule.match(exp)
    if not mc:
        return qs

    M = qs.model
    models = [qs.model]
    for k in qs._joins:
        val = qs._joins[k]
        for item in val:
            models.append(item[0])

    target, col, op, val = mc.groups()
    for M in models:
        if M._meta.table_name == target:
            qs, col = get_obj_attr(qs, M, col)
            val = get_val(val, context)
            _exp = comparison_operators[op](col, val)
            qs = qs.where(_exp)
    return qs

