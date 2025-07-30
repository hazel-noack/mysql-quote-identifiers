from mysql_quote_identifiers import escape_identifier


if __name__ == "__main__":
    print(escape_identifier("foo-bar"))
