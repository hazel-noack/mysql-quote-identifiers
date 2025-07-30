import unittest
import logging
from mysql_quote_identifiers import escape_identifier, IdentifierException


logger = logging.getLogger("mysql_quote_identifiers")


class TestGeneralQuoted(unittest.TestCase):
    pass


class TestGeneralUnQuoted(unittest.TestCase):
    def test_reserve_words(self):
        random_reserved_words = ['SQLWARNING', 'BETWEEN', 'LOCALTIMESTAMP', 'DOUBLE', 'TRAILING', 'ENCLOSED', 'DELAYED', 'SQLWARNING', 'OPTION', 'SCHEMAS']

        for reserved_word in random_reserved_words:
            with self.assertRaises(IdentifierException):
                escape_identifier(reserved_word, is_quoted=False, oracle_mode=False)

    def test_reserve_words_no_oracle_mode(self):
        random_reserved_words = ['ROWTYPE', 'SYSTEM', 'RAISE', 'SYSTEM', 'VERSIONING', 'ROWTYPE', 'ROWTYPE', 'PACKAGE', 'RAISE']

        for reserved_word in random_reserved_words:
            self.assertEqual(escape_identifier(reserved_word, is_quoted=False, oracle_mode=False), reserved_word)

    def test_reserve_words_oracle_mode(self):
        random_reserved_words = ['ROWTYPE', 'SYSTEM', 'RAISE', 'SYSTEM', 'VERSIONING', 'ROWTYPE', 'MINUS (> 10.6.0)', 'ROWTYPE', 'PACKAGE', 'RAISE']

        for reserved_word in random_reserved_words:
            with self.assertRaises(IdentifierException):
                escape_identifier(reserved_word, is_quoted=False, oracle_mode=True)


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

    """
    Identifiers are not permitted to contain the ASCII NUL character (U+0000) and supplementary characters (U+10000 and higher).
    """
    def test_no_null(self):
        with self.assertRaises(IdentifierException):
            escape_identifier("foo\u0000bar", is_quoted=True)

    def test_no_supplementary(self):
        with self.assertRaises(IdentifierException):
            escape_identifier("foo\U00010000bar", is_quoted=True)

        with self.assertRaises(IdentifierException):
            escape_identifier("foo\U00010200bar", is_quoted=True)
        
        with self.assertRaises(IdentifierException):
            escape_identifier("foo\U00010060bar", is_quoted=True)

        with self.assertRaises(IdentifierException):
            escape_identifier("foo\U00010670bar", is_quoted=True)

    def test_ambiguity(self):
        """
        Names such as 5e6, 9e are not prohibited, but it's strongly recommended not to use them, as they could lead to ambiguity in certain contexts, being treated as a number or expression.
        """

        with self.assertLogs(logger, level=logging.WARNING) as cm:
            escape_identifier("5e6", is_quoted=True)
            self.assertIn(
                "WARNING:mysql_quote_identifiers:names such as 5e6, 9e are not prohibited, but it's strongly recommended not to use them, as they could lead to ambiguity in certain contexts, being treated as a number or expression", 
                cm.output
            )

        with self.assertLogs(logger, level=logging.WARNING) as cm:
            escape_identifier("9e", is_quoted=True)
            self.assertIn(
                "WARNING:mysql_quote_identifiers:names such as 5e6, 9e are not prohibited, but it's strongly recommended not to use them, as they could lead to ambiguity in certain contexts, being treated as a number or expression", 
                cm.output
            )

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

    """
    Identifiers are not permitted to contain the ASCII NUL character (U+0000) and supplementary characters (U+10000 and higher).
    """
    def test_no_null(self):
        with self.assertRaises(IdentifierException):
            escape_identifier("foo\u0000bar", is_quoted=False)

    def test_no_supplementary(self):
        with self.assertRaises(IdentifierException):
            escape_identifier("foo\U00010000bar", is_quoted=False)

        with self.assertRaises(IdentifierException):
            escape_identifier("foo\U00010200bar", is_quoted=False)
        
        with self.assertRaises(IdentifierException):
            escape_identifier("foo\U00010060bar", is_quoted=False)

        with self.assertRaises(IdentifierException):
            escape_identifier("foo\U00010670bar", is_quoted=False)
