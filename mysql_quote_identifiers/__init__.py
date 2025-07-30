import pathlib


__name__ = "mysql_quote_identifiers"
__folder__ = str(pathlib.Path(__file__).parent)


# https://stackoverflow.com/questions/51867550/pymysql-escaping-identifiers
# https://mariadb.com/docs/server/reference/sql-structure/sql-language-structure/identifier-names
def quote_identifier(identifier: str) -> str:
    return identifier
