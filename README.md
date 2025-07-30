# Mysql-Quote-Identifiers

The python mysql connector has no way to safely quote identifiers like table names or database names. This library implements basic functions to do that.  
If you find a security vulnerability PLEASE open an issue or a pull request.

I tried to strictly work with the [mariadb specs on identifier names](https://mariadb.com/docs/server/reference/sql-structure/sql-language-structure/identifier-names).

## Limitations

User variables cannot be used as part of an identifier, or as an identifier in an SQL statement.

## License

This library uses the MIT License. Do whatever you want with it.
