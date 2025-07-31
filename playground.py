from mysql_quote_identifiers import escape_identifier, IdentifierException, IdentifierType,  SqlMode


print(escape_identifier("foo-bar")) # > foo-bar
print(escape_identifier("foo`bar")) # > foo``bar


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
print(escape_identifier('foo"bar', sql_mode=[SqlMode.ANSI_QUOTES])) # > foo""bar
