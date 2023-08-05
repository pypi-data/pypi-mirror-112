import pytest
from collections import Counter
from icecream import ic
from limeutils import utils, listify, valid_str_only


param = [(3, True), (3.0, True), (0, True), ('3.4', True), ('0.4', True), ('0.0', True),
         ('0', True), ('3.0', True), ('3', True), ('abc', False), ('3,344', False),
         ('3,344.5', False), ('3,344.00', False)]
@pytest.mark.parametrize('val, out', param)
def test_isfloat(val, out):
    assert utils.isfloat(val) is out


param = [('123', 123), ('12.3', 12.3), ('a1b2c3', 'a1b2c3'), ('abc', 'abc'), ('', ''), ('-', '-'),
         (None, ValueError), (bytes(), ValueError), ('True', True), ('False', False),]
@pytest.mark.parametrize('val, out', param)
def test_parse_str(val, out):
    try:
        assert utils.parse_str(val) == out
    except out:
        with pytest.raises(out):
            assert utils.parse_str(val)


param = [('Hey You', ('Hey', 'You')), ('Sir Hey You', ('Sir Hey', 'You')),
         ('Sir Hey You Phd', ('Sir Hey', 'You Phd')), ('Hey delos You', ('Hey', 'delos You')),
         ('Hey san You', ('Hey', 'san You')),
         ('Eliza Maria Erica dona Aurora Phd Md', ('Eliza Maria Erica', 'dona Aurora Phd Md'))]
@pytest.mark.parametrize('val, out', param)
def test_split_fullname(val, out):
    assert utils.split_fullname(val) == out


param = [('abra', 'fed'), ('abra', 6.22), ('abra', 789), ('abra', '1.5'), ('abra', '123')]
@pytest.mark.parametrize('key, val', param)
def test_byte_conv(red, key, val):
    red.set(key, val)
    if val == '123':
        val = 123
    if val == '1.5':
        val = 1.5
    assert red.get(key) == val


param = [
    (['one', 'two', 'three', 'four'], 'one, two, three, or four'),
    (['one', 'two', 'three'], 'one, two, or three'),
    (['one', 'two'], 'one or two'),
    (['one'], 'one'), ([], '')
]
@pytest.mark.parametrize('seq, out', param)
@pytest.mark.utilfocus
def test_oxford_comma(seq, out):
    assert utils.oxford_comma(seq) == out


param = [
    ('foo', ['foo']), (['foo'], ['foo']),
    (1, [1]), (12.5, [12.5]),
    (['foo', 'bar'], ['foo', 'bar']),
    (('foo',), ['foo']), (('foo', 'bar'), ['foo', 'bar']),
    ({'foo'}, ['foo']), ({'foo', 'bar'}, ['foo', 'bar']),
    (True, [True]), (False, [False])
]
@pytest.mark.parametrize('data, out', param)
# @pytest.mark.focus
def test_listify(data, out):
    assert Counter(listify(data)) == Counter(out)


param = [
    ('', False, False), ([], False, False), (None, False, False), (1, False, False),
    (1.5, False, False), (False, False, False), (True, False, False), ('a', False, True),
    (set(), False, False), ('', False, False), (True, True, True), (False, True, False)
]
@pytest.mark.parametrize('item, allow, out', param)
@pytest.mark.focus
def test_valid_str_only(item, allow, out):
    if allow:
        assert valid_str_only(item, allow_bool=True) == out
    else:
        assert valid_str_only(item) == out
        