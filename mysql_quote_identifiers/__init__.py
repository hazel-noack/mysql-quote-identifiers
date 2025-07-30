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
def escape_identifier(
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

    # Identifier names may begin with a numeral, but can't only contain numerals unless quoted.
    if not is_quoted:
        if identifier.isnumeric():
            raise IdentifierException("identifier names may begin with a numeral, but can't only contain numerals unless quoted")

    # An identifier starting with a numeral, followed by an 'e', may be parsed as a floating point number, and needs to be quoted.
    if not is_quoted:
        for char in identifier:
            if char.isnumeric():
                continue

            if char == "e":
                raise IdentifierException("an identifier starting with a numeral, followed by an 'e', may be parsed as a floating point number, and needs to be quoted")
            else:
                break

    # Identifiers are not permitted to contain the ASCII NUL character (U+0000) and supplementary characters (U+10000 and higher).
    for char in identifier:
        print(ord(char))

    return identifier
