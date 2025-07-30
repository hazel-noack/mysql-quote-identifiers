import random
from mysql_quote_identifiers import escape_identifier
from mysql_quote_identifiers.reserved_words import RESERVED_WORDS, RESERVED_WORDS_ORACLE_MODE


if __name__ == "__main__":
    print(random.choices(list(RESERVED_WORDS), k=10))
