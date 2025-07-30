from mysql_quote_identifiers import quote_identifier


def p_quote_identifier(i):
    print(quote_identifier(i))


if __name__ == "__main__":
    print("testing script")
    quote_identifier("test test")
