# -*- coding: utf-8 -*-
import pytest  # noqa
from parglare import Parser, GLRParser, Grammar
from ..grammar.expression_grammar import get_grammar


def test_to_str():

    grammar = get_grammar()
    p = Parser(grammar, build_tree=True)

    res = p.parse("""id+  id * (id
    +id  )
    """)

    ts = res.to_str()

    assert '+[18->19, "+"]' in ts
    assert ')[23->24, ")"]' in ts
    assert 'F[10->24]' in ts


def test_forest_to_str():

    grammar = Grammar.from_string(r'''
    E: E "+" E | E "-" E | "(" E ")" | "id";
    ''')
    p = GLRParser(grammar)

    forest = p.parse("""id+  id - (id
    +id  )
    """)

    ts = forest.to_str()

    assert 'E - ambiguity[2]' in ts
    assert 'E[10->24]' in ts
    assert '      E[11->21]' in ts
    assert '        +[18->19, "+"]' in ts
