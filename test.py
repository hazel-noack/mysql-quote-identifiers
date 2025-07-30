import unittest
import logging
from mysql_quote_identifiers import escape_identifier, IdentifierException


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
            escape_identifier("foo ", is_quoted=True)

    def test_allow_numeric(self):
        """
        Identifier names may begin with a numeral, but can't only contain numerals unless quoted.
        """
            
        self.assertEqual(escape_identifier("1234", is_quoted=True), "1234")

    def test_allow_float(self):
        self.assertEqual(escape_identifier("1234e", is_quoted=True), "1234e")


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
            escape_identifier("foo ", is_quoted=False)

    """
    Identifier names may begin with a numeral, but can't only contain numerals unless quoted.
    """

    def test_numeric(self):
        with self.assertRaises(IdentifierException):
            escape_identifier("1234", is_quoted=False)

    def test_non_numeric(self):
        self.assertEqual(escape_identifier("1d", is_quoted=False), "1d")

    """
    An identifier starting with a numeral, followed by an 'e', may be parsed as a floating point number, and needs to be quoted.
    """
    def test_no_float(self):
        with self.assertRaises(IdentifierException):
            escape_identifier("1234e", is_quoted=False)
    
    def test_other_no_float(self):
        with self.assertRaises(IdentifierException):
            escape_identifier("1234efg", is_quoted=False)

    def test_is_no_float(self):
        self.assertEqual(escape_identifier("1234de", is_quoted=False), "1234de")
