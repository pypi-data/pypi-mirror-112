import re
from camtono.parser.format import BaseFormatter


def format_query(query_ast):
    query = BigQueryFormatter().format(query_ast)
    query = clean_table_names(query=query)
    query = update_regex_pattern(query=query)

    return query


def clean_table_names(query):
    return re.sub('("[\S]+\.[\S]+\.[\S]+")', replace_quotes, query)


def replace_quotes(m):
    return m.string[m.span()[0]:m.span()[1]].replace('"', '`')


def format_schema(column_name, data_type: str):
    mode = 'nullable'
    if data_type.lower().startswith('array'):
        mode = 'repeated'
        if '<' in data_type:
            data_type = data_type.lower().replace('array<', '').replace('>', '')
        else:
            data_type = 'string'
    elif data_type in {'json', 'jsonb'}:
        data_type = 'struct'
    return dict(name=column_name, mode=mode, type=data_type)


def update_regex_pattern(query):
    return query.replace("\\", "\\\\")


class BigQueryFormatter(BaseFormatter):
    pass
