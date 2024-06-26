from gendiff.const import DIFF_CHANGES_TYPES
from gendiff.const import INDENTS_FORMATS


def formatted_data(data):
    match data:
        case False | True:
            return str(data).lower()
        case None:
            return 'null'
        case _:
            return str(data)


def make_tree(data, depth, indent='    '):
    result = []

    def make(data, depth):
        if not isinstance(data, dict):
            result.append(f'{formatted_data(data)}\n')
        else:
            result.append('{\n')
            for key, value in data.items():
                depth += 1
                result.append(f'{indent * depth}{indent}{key}: ')
                _ = make(value, depth)
                depth -= 1
            result.append(f'{indent * depth}{indent}}}\n')
    make(data, depth)
    return result


def make_stylish(diff):
    result = ['{\n']
    indent = INDENTS_FORMATS.INDENT
    indent_add = INDENTS_FORMATS.INDENT_ADD
    indent_del = INDENTS_FORMATS.INDENT_DEL

    def make_result(data, depth=0):
        for key, value in data.items():
            status = value.get('status')
            value_file = value.get('value')
            old_value_file = value.get('old_value')
            new_value_file = value.get('new_value')
            children = value.get('children')
            match status:
                case DIFF_CHANGES_TYPES.ADDED:
                    result.append(f'{indent * depth}{indent_add}{key}: ')
                    result.extend(make_tree(value_file, depth))
                case DIFF_CHANGES_TYPES.DELETED:
                    result.append(f'{indent * depth}{indent_del}{key}: ')
                    result.extend(make_tree(value_file, depth))
                case DIFF_CHANGES_TYPES.UNCHANGED:
                    result.append(f'{indent * depth}{indent}{key}: ')
                    result.extend(make_tree(value_file, depth))
                case DIFF_CHANGES_TYPES.CHANGED:
                    result.append(f'{indent * depth}{indent_del}{key}: ')
                    result.extend(make_tree(old_value_file, depth))
                    result.append(f'{indent * depth}{indent_add}{key}: ')
                    result.extend(make_tree(new_value_file, depth))
                case _:
                    result.append(f'{indent * depth}{indent}{key}: {{\n')
                    depth += 1
                    _ = make_result(children, depth)
                    depth -= 1
                    result.append(f'{indent * depth}{indent}}}\n')
        return result
    make_result(diff)
    result.append('}')
    return ''.join(result)
