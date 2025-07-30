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

    def test_allow_numeric(self):
        self.assertEqual(escape_quoted_identifier("1234", is_quoted=True), "1234")


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

    """
    Identifier names may begin with a numeral, but can't only contain numerals unless quoted.
    """

    def test_numeric(self):
        with self.assertRaises(IdentifierException):
            escape_quoted_identifier("1234", is_quoted=False)

    def test_non_numeric(self):
        self.assertEqual(escape_quoted_identifier("1d", is_quoted=False), "1d")

