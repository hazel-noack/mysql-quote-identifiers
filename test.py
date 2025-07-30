import unittest
import logging
from mysql_quote_identifiers import escape_quoted_identifier, IdentifierException


logger = logging.getLogger("mysql_quote_identifiers")


class TestFurtherRulesQuoted(unittest.TestCase):
    """
    Testing the further rules section of the spec
    https://mariadb.com/docs/server/reference/sql-structure/sql-language-structure/identifier-names#further-rules
    """
    def test_whitespaces(self):
        """
        Database, table and column names can't end with space characters
        """
        with self.assertRaises(IdentifierException):
            escape_quoted_identifier("foo ", is_quoted=True)


class TestFurtherRulesUnQuoted(unittest.TestCase):
    """
    Testing the further rules section of the spec
    https://mariadb.com/docs/server/reference/sql-structure/sql-language-structure/identifier-names#further-rules
    """
    def test_whitespaces(self):
        """
        Database, table and column names can't end with space characters
        """
        with self.assertRaises(IdentifierException):
            escape_quoted_identifier("foo ", is_quoted=False)

