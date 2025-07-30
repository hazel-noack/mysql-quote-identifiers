import unittest
import logging
from mysql_quote_identifiers import quote_identifier, IdentifierException, IdentifierType


logger = logging.getLogger("mysql_quote_identifiers")


class TestFurtherRules(unittest.TestCase):
    """
    Testing the further rules section of the spec
    https://mariadb.com/docs/server/reference/sql-structure/sql-language-structure/identifier-names#further-rules
    """
    def test_whitespaces(self):
        """
        Database, table and column names can't end with space characters
        """
        with self.assertRaises(IdentifierException):
            quote_identifier("foo ", IdentifierType.DATABASE)
