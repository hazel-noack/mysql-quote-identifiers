from mysql_quote_identifiers import quote_identifier


def p_quote_identifier(i):
    pad_char = ""
    print(f"{i:{pad_char}<30} => `{quote_identifier(i)}`")


if __name__ == "__main__":
    p_quote_identifier("test test")
    p_quote_identifier("test test \\")
    p_quote_identifier("test`; SELECT * FROM user")
