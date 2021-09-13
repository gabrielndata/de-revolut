from nest import utils


def test_convert_to_hashable(folded_data):
    d = {
        'a': {
            'b': [
                {'c': 1, 'b': 2},
                {'a': 1, 'b': 2},
            ],
            'c': [1, 2, 3, [5, 6]],
            'd': {'a': {'b':[1 , 2]}}
        }
    }
    hashable = set(utils.tupleit(d))
    assert hashable == {
        ('a', (
            'b', (
                ('c', 1), ('b', 2)), (('a', 1), ('b', 2))),
                          ('c', 1, 2, 3, (5, 6)), ('d', ('a', ('b', 1, 2))))}