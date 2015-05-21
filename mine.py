from utils import get_subtables, formalize_rules, is_mono
from c45 import gain
import json, logging
from datetime import date, timedelta, datetime


def mine_c45(table, result):
    tree = []
    cols = [(k, gain(table, k, result)) for k in table.keys() if k != result]
    if(len(cols) > 0):
        cols = max(cols, key=lambda x: x[1])
        col = cols[0]
        for subt in get_subtables(table, col):
            v = subt[col][0]
            if is_mono(subt[result]):
                tree.append(['%s=%s' % (col, v),
                             '%s=%s' % (result, subt[result][0])])
            else:
                del subt[col]
                mine_result = mine_c45(subt, result)
                if(len(mine_result) > 0):
                    tree.append(['%s=%s' % (col, v)] + mine_result)
    return tree

def tree_to_rules(tree):
    return formalize_rules(__tree_to_rules(tree))


def __tree_to_rules(tree, rule=''):
    rules = []
    for node in tree:
        if isinstance(node, basestring):
            rule += node + ','
        else:
            rules += __tree_to_rules(node, rule)
    if rules:
        return rules
    return [rule]


def validate_table(table):
    assert isinstance(table, dict)
    for k, v in table.items():
        assert k
        assert isinstance(k, basestring)
        assert len(v) == len(table.values()[0])
        for i in v: assert i

#table = json.loads(open('stock.json').read())
#tree = mine_c45(table, 'result')
#str_rules = tree_to_rules(tree)
str_rules="3213"
logging.basicConfig(filename= datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+ '.log',level=logging.DEBUG)
logging.info(str_rules)
logging.shutdown()
