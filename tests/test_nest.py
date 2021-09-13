from nest.controller import nestify


def test_nested_contains(nested_dict):
    nested_dict['d']['e'] = [1, 2, 3]
    assert 'e' in nested_dict


def test_nested_set(nested_dict):
    nested_dict['a'] = 1
    assert nested_dict['a'] == 1


def test_nested_get(nested_dict):
    assert nested_dict['b'] == {}


def test_nested_group_original(flat_data, folded_data):
    nested_dict = nestify(flat_data, 'currency', 'country', 'city')
    assert nested_dict == folded_data
    assert 'USD' in nested_dict
    assert nested_dict['EUR']['ES']['Madrid'][0]['amount'] == 8.9


def test_nested_group_by_country(flat_data):
    nested_dict = nestify(flat_data, 'country', 'city', 'currency')
    assert nested_dict['ES']['Madrid']['EUR'][0]['amount'] == 8.9


def test_nested_group_by_city(flat_data):
    nested_dict = nestify(flat_data, 'city', 'currency', 'country')
    assert nested_dict['Madrid']['EUR']['ES'][0]['amount'] == 8.9


def test_nested_group_by_one_key(flat_data):
    nested_dict = nestify(flat_data, 'city')
    assert nested_dict['Madrid'][0]['amount'] == 8.9


def test_nested_group_by_none(flat_data):
    nested_dict = nestify(flat_data)
    assert nested_dict['root'] == flat_data


def test_nested_group_by_none_exits(flat_data):
    nested_dict = nestify(flat_data, 'hello')
    assert nested_dict['root'] == flat_data
