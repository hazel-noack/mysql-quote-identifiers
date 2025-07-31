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
```

## Limitations

> User variables cannot be used as part of an identifier, or as an identifier in an SQL statement.

There is no way I can get the user variables properly, thus I also can not validate those. So a sql injection where the attacker puts a user variable in that reveals something **might** be possible.

## License

This library uses the MIT License. Do whatever you want with it.
