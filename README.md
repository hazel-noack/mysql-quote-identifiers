# Mysql-Quote-Identifiers

The python mysql connector has no way to safely quote identifiers like table names or database names. This library implements basic functions to do that.  
If you find a security vulnerability PLEASE open an issue or a pull request.

I tried to strictly work with the [mariadb specs on identifier names](https://mariadb.com/docs/server/reference/sql-structure/sql-language-structure/identifier-names).

## Installation

```sh
pip install mysql-quote-identifiers
```

## Usage

The main function is `mysql_quote_identifiers.escape_identifier`.

It validates and escapes quoted identifiers, because that is way safer, but it can also do that with unquoted identifiers. If you want this, set the argument `is_quoted` to `False`. However, I **STRONGLY recommend not doing that**.

If you use it with quoted identifiers, the library will either automatically wrap the identifier in the quotes, or will validate if the quotes are there.

The library escapes the identifiers, and raises `IdentifierException` where it can't. If you only want to validate the identifier, you can add the argument `only_validate`.

MariaDB has the `SQL_MODE` flag `ANSI_QUOTES`. This changes the quoting character from a backtick `` ` `` to a normal quote `"`. You can enable this by turning on by passing `sql_mode=[SqlMode.ANSI_QUOTES]` in the function. **IMPORTANT:** if that isn't configured correctly it opens up your software to sql injection so try out what the mode on you server is.

```python
from mysql_quote_identifiers import escape_identifier, IdentifierException, IdentifierType,  SqlMode


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

```

A minor detail is, that you cant use [reserved words](https://mariadb.com/docs/server/reference/sql-structure/sql-language-structure/reserved-words) with unquoted identifiers. If [ORACLE mode](https://mariadb.com/docs/release-notes/community-server/about/compatibility-and-differences/sql_modeoracle) is enabled there are more reserved words that can be used. You can enable it by passing `SqlMode.ORACLE` in the function.

```python
escape_identifier("foo", is_quoted=False, sql_mode=[SqlMode.ORACLE])
```

### Use Case

Here is an example how you can use this library as safely as possible:

```python
from mysql_quote_identifiers import escape_identifier, IdentifierType


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
```

As you can see this escapes + validates the identifiers and protects sql injections from happening. Here is an example of an sql injection being prevented:

```
table to create: foo`; SELECT * FROM users;
column to create: bar

CREATE TABLE `foo``; SELECT * FROM users;` (
    `id` int,
    `bar` varchar(255)
);
```

If you want to you can try running it and confirm it working.

### Best Practices

Here are the best practices to follow to make it as secure as possible:

1. always use quoted identifiers
2. always check if `ANSI_QUOTES` is set
3. always check if `ORACLE MODE` is set


## Limitations

> User variables cannot be used as part of an identifier, or as an identifier in an SQL statement.

There is no way I can get the user variables properly, thus I also can not validate those. So a sql injection where the attacker puts a user variable in that reveals something **might** be possible.

## License

This library uses the MIT License. Do whatever you want with it.
