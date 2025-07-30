from typing import Optional, List
from enum import Enum
import logging
import re

from .reserved_words import RESERVED_WORDS, RESERVED_WORDS_ORACLE_MODE


logger = logging.getLogger("mysql_quote_identifiers")


class IdentifierException(Exception):
    pass


class SqlMode(Enum):
    ANSI_QUOTES = 0


"""
UNQUOTED
The following characters are valid, and allow identifiers to be unquoted:
- ASCII: [0-9,a-z,A-Z$_] (numerals 0-9, basic Latin letters, both lowercase and uppercase, dollar sign, underscore)
- Extended: U+0080 .. U+FFFF
"""
unquoted_allowed = re.compile(r'^[0-9a-zA-Z_\$\u0080-\uFFFF]+$')
"""
QUOTED
The following characters are valid, but identifiers using them must be quoted:
    ASCII: U+0001 .. U+007F (full Unicode Basic Multilingual Plane (BMP) except for U+0000)
    Extended: U+0080 .. U+FFFF
    CANT DO THIS HERE: Identifier quotes can themselves be used as part of an identifier, as long as they are quoted.
"""
quoted_allowed = re.compile(r'^[\u0001-\u007F\u0080-\uFFFF]+$')


# https://stackoverflow.com/questions/51867550/pymysql-escaping-identifiers
# https://mariadb.com/docs/server/reference/sql-structure/sql-language-structure/identifier-names
def escape_identifier(
    identifier: str,
    is_quoted: bool = False,
    oracle_mode: bool = False,
    sql_mode: Optional[List[SqlMode]] = None,
    allow_edit: bool = True,
) -> str:
    # check if all characters in the identifier are allowed
    allowed_characters = quoted_allowed if is_quoted else unquoted_allowed
    if not allowed_characters.match(identifier):
        raise IdentifierException("identifier used illegal characters")

    # Quoting is optional for identifiers that are not reserved words.
    if not is_quoted:
        reserved = RESERVED_WORDS if not oracle_mode else RESERVED_WORDS_ORACLE_MODE
        if identifier in reserved:
            raise IdentifierException("unquoted identifiers can not be reserved words")
        
    # quote characters
    # https://mariadb.com/docs/server/reference/sql-structure/sql-language-structure/identifier-names#quote-character
    sql_mode = [] if sql_mode is None else sql_mode
    quote_char = '"' if SqlMode.ANSI_QUOTES in sql_mode else '`'
    if is_quoted:
        if allow_edit:
            identifier = identifier.replace(quote_char, quote_char + quote_char)
        else:
            count = 0
            for char in identifier:
                if char == quote_char:
                    count += 1
                else:
                    if count % 2 != 0:
                        raise IdentifierException(f"the quote char {quote_char} needs to be escaped")

                    count = 0
    else:
        if quote_char in identifier:
            raise IdentifierException(f"unquoted identifiers cant contain the quote char {quote_char}")

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
        numeric = ord(char)
        if numeric == 0 or numeric >= 0x10000:
            raise IdentifierException("identifiers are not permitted to contain the ASCII NUL character (U+0000) and supplementary characters (U+10000 and higher)")

    # Names such as 5e6, 9e are not prohibited, but it's strongly recommended not to use them, as they could lead to ambiguity in certain contexts, being treated as a number or expression.
    if identifier.replace("e", "", 1).isnumeric():
        logger.warning("names such as 5e6, 9e are not prohibited, but it's strongly recommended not to use them, as they could lead to ambiguity in certain contexts, being treated as a number or expression")

    return identifier
