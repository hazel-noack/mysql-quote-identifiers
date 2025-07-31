# Mysql-Quote-Identifiers

The python mysql connector has no way to safely quote identifiers like table names or database names. This library implements basic functions to do that.  
If you find a security vulnerability PLEASE open an issue or a pull request.

I tried to strictly work with the [mariadb specs on identifier names](https://mariadb.com/docs/server/reference/sql-structure/sql-language-structure/identifier-names).

## Installation

```sh
pip install mysql-quote-identifiers
```

## Usage

```python
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
```

## Limitations

> User variables cannot be used as part of an identifier, or as an identifier in an SQL statement.

There is no way I can get the user variables properly, thus I also can not validate those. So a sql injection where the attacker puts a user variable in that reveals something **might** be possible.

## License

This library uses the MIT License. Do whatever you want with it.
