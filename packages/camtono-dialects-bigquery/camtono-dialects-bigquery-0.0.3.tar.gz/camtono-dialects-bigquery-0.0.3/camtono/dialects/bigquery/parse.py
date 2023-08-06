from camtono.parser.parse import Parser


def parse_query(query):
    return BigQueryParser().parse(query)


class BigQueryParser(Parser):
    pass
