from mysql_quote_identifiers import escape_identifier, IdentifierException, IdentifierType,  SqlMode


def demo():
    print(escape_identifier("foo-bar")) # > `foo-bar`
    print(escape_identifier("foo`bar")) # > `foo``bar`
    print(escape_identifier("foo_bar", is_quoted=False))    # > foo_bar


    # you can also use this for unquoted fields
    try:
        escape_identifier("foo-bar", is_quoted=False)
    except IdentifierException as e:
        print(e)    # > identifier used illegal characters


    # you should also always specify the identifier type
    try:
        print(escape_identifier("foo-bar ", identifier_type=IdentifierType.DATABASE))
    except IdentifierException as e:
        print(e)    # > database, table and column names can't end with space characters

    # you can also use the ANSI_QUOTE SQL_MODE
    print(escape_identifier('foo"bar', sql_mode=[SqlMode.ANSI_QUOTES])) # > "foo""bar"


EXAMPLE_QUERY = """
CREATE TABLE {table} (
    `id` int,
    {column} varchar(255)
); 
"""

def use_case():
    table = input("table to create: ")
    column = input("column to create: ")

    # like you can see, the quotes are added automatically, so they don't have to be in the template
    print(EXAMPLE_QUERY.format(
        table = escape_identifier(table, identifier_type=IdentifierType.TABLE),
        column = escape_identifier(column, identifier_type=IdentifierType.COLUMN)
    ))


if __name__ == "__main__":
    use_case()
