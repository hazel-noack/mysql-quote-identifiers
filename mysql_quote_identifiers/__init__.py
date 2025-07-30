__name__ = "mysql_quote_identifiers"


MALICIOUS_CHARACTER = ["`", "\\"]


# https://stackoverflow.com/questions/51867550/pymysql-escaping-identifiers
# https://mariadb.com/docs/server/reference/sql-structure/sql-language-structure/identifier-names
def quote_identifier(identifier: str) -> str:
    quoted = ""
    for char in identifier:
        if char in MALICIOUS_CHARACTER:
            char = "\\" + char
        
        quoted += char

    return quoted
