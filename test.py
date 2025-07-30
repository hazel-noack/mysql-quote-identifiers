import unittest
import logging
from mysql_quote_identifiers import escape_identifier, IdentifierException, SqlMode, IdentifierType


logger = logging.getLogger("mysql_quote_identifiers")


class TestQuoteChars(unittest.TestCase):
    def test_unquoted(self):
        with self.assertRaises(IdentifierException):
            escape_identifier("meow``meow", is_quoted=False)

        with self.assertRaises(IdentifierException):
            escape_identifier("meow`meow", is_quoted=False)

        with self.assertRaises(IdentifierException):
            escape_identifier('meow""meow', is_quoted=False, sql_mode=[SqlMode.ANSI_QUOTES])

        with self.assertRaises(IdentifierException):
            escape_identifier('meow"meow', is_quoted=False, sql_mode=[SqlMode.ANSI_QUOTES])

    def test_escaping(self):
        self.assertEqual(
            escape_identifier("meow`meow", is_quoted=True, allow_edit=True),
            "meow``meow",
        )

        self.assertEqual(
            escape_identifier("meow``meow", is_quoted=True, allow_edit=True),
            "meow````meow",
        )

        self.assertEqual(
            escape_identifier("m`eow``meow", is_quoted=True, allow_edit=True),
            "m``eow````meow",
        )

        self.assertEqual(
            escape_identifier(
                'meow"meow', 
                is_quoted=True, 
                sql_mode=[SqlMode.ANSI_QUOTES],
                allow_edit=True,
            ),
            'meow""meow',
        )

    def test_validating(self):
        with self.assertRaises(IdentifierException):
            escape_identifier("meow`meow", is_quoted=True, allow_edit=False)

        with self.assertRaises(IdentifierException):
            escape_identifier("meow```meow", is_quoted=True, allow_edit=False)

        with self.assertRaises(IdentifierException):
            escape_identifier("me`ow``meow", is_quoted=True, allow_edit=False)


        self.assertEqual(
            escape_identifier("meow``meow", is_quoted=True, allow_edit=False),
            "meow``meow",
        )

        self.assertEqual(
            escape_identifier("meow````meow", is_quoted=True, allow_edit=False),
            "meow````meow",
        )

        self.assertEqual(
            escape_identifier("m``eow``meow", is_quoted=True, allow_edit=False),
            "m``eow``meow",
        )

        with self.assertRaises(IdentifierException):
            escape_identifier('meow"meow', is_quoted=True, allow_edit=False, sql_mode=[SqlMode.ANSI_QUOTES])

        self.assertEqual(
            escape_identifier('meow""meow', is_quoted=True, allow_edit=False, sql_mode=[SqlMode.ANSI_QUOTES]),
            'meow""meow',
        )


class TestGeneralQuoted(unittest.TestCase):
    def test_legal_characters(self):
        cases = [
            "foo_bar",
            "foo_bar_baz",
            "ä",
            "meow",
            "test$test",
            "with space",
            "foo-bar",
            "foo-bar-baz",
            "test$test^",
        ]

        for c in cases:
            self.assertEqual(escape_identifier(c, is_quoted=True), c)

    def test_illegal_characters(self):
        cases = [
            "test$test^\U00010000"
        ]

        for c in cases:
            with self.assertRaises(IdentifierException):
                escape_identifier(c, is_quoted=True)

class TestGeneralUnQuoted(unittest.TestCase):
    def test_legal_characters(self):
        cases = [
            "foo_bar",
            "foo_bar_baz",
            "ä",
            "meow",
            "test$test"
        ]

        for c in cases:
            self.assertEqual(escape_identifier(c, is_quoted=False), c)

    def test_illegal_characters(self):
        cases = [
            "with space",
            "foo-bar",
            "foo-bar-baz",
            "test$test^",
        ]

        for c in cases:
            with self.assertRaises(IdentifierException):
                escape_identifier(c, is_quoted=False)


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

        with self.assertRaises(IdentifierException):
            escape_identifier("foo ", is_quoted=True, identifier_type=IdentifierType.COLUMN)
        
        with self.assertRaises(IdentifierException):
            escape_identifier("foo ", is_quoted=True, identifier_type=IdentifierType.DATABASE)

    def test_whitespaces_allowed(self):
        self.assertEqual(
            escape_identifier(
                "foo ", 
                is_quoted=True, 
                identifier_type=IdentifierType.SERVER
            ),
            "foo ",
        )

        self.assertEqual(
            escape_identifier(
                "foo ", 
                is_quoted=True, 
                identifier_type=IdentifierType.ALIAS
            ),
            "foo ",
        )

        self.assertEqual(
            escape_identifier(
                "foo ", 
                is_quoted=True, 
                identifier_type=IdentifierType.COMPOUND_STATEMENT
            ),
            "foo ",
        )

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
