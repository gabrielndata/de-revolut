from .data_struct import NestedDefaultDict


def nestify(dicts, *keys) -> NestedDefaultDict:
    """
    Group provided dictionaries by values acquired from provided keys in order::

        nestify([{'currency': "USD", 'country': 'US'}...], 'currency', 'country'...)

    :param list[dict] dicts:        list of objects you want to group
    :param str keys:          keys to group objects by. Non existing keys will be ignored
    :rtype: NestedDefaultDict
    :return:
    """
    nested = NestedDefaultDict()
    nested.group_by_values(dicts, *keys)
    return nested
