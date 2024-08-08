import unittest
from unittest.mock import MagicMock, patch
from src.db_conn import DBEngine


class TestDBEngine(unittest.TestCase):
    @patch('src.db_conn.st.connection')
    def test_db_engine_init(self, mock_connect):
        mock_connection = MagicMock(name='mock_connection')
        mock_connect.return_value = mock_connection
        db_engine = DBEngine()

        assert db_engine.connection == mock_connection

    @patch('src.db_conn.st.connection')
    def test_db_engine_del(self, mock_connect):
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        db_engine = DBEngine()
        del db_engine
        mock_connection.session.close.assert_called_once()
