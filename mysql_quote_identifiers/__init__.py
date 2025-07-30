from enum import Enum
import logging


logger = logging.getLogger("mysql_quote_identifiers")


class IdentifierException(Exception):
    pass


class IdentifierType(Enum):
    DATABASE = 0
    TABLE = 1
    COLUMN = 2


class ANSI_QUOTES(Enum):
    BACKTICKS = '`'
    DOUBLE_QUOTES = '"'
    SQUARE_BRACKETS = '[]'


MALICIOUS_CHARACTER = ["`", "\\"]


# https://stackoverflow.com/questions/51867550/pymysql-escaping-identifiers
# https://mariadb.com/docs/server/reference/sql-structure/sql-language-structure/identifier-names
def escape_quoted_identifier(
    identifier: str,
    is_quoted: bool = False
) -> str:
    quoted = ""
    for char in identifier:
        if char in MALICIOUS_CHARACTER:
            char = "\\" + char
        
        quoted += char
    identifier = quoted

    # implementing further rules https://mariadb.com/docs/server/reference/sql-structure/sql-language-structure/identifier-names#further-rules
    # Database, table and column names can't end with space characters
    if identifier.endswith(" "):
        raise IdentifierException("database, table and column names can't end with space characters")

    return identifier
