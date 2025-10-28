"""Tests for OmnivoxClient."""

import unittest
from unittest.mock import Mock, patch, MagicMock
from omnivox import OmnivoxClient
from omnivox.exceptions import AuthenticationError


class TestOmnivoxClient(unittest.TestCase):
    """Test cases for OmnivoxClient class."""
    
    @patch('omnivox.client.OmnivoxAuth')
    @patch('omnivox.client.LeaManager')
    @patch('omnivox.client.MioManager')
    def test_successful_initialization(self, mock_mio, mock_lea, mock_auth):
        """Test successful client initialization."""
        # Mock authentication
        mock_auth_instance = Mock()
        mock_auth_instance.login.return_value = True
        mock_auth_instance.is_authenticated = True
        mock_auth_instance.get_session.return_value = Mock()
        mock_auth.return_value = mock_auth_instance
        
        # Create client
        client = OmnivoxClient("1234567", "password")
        
        # Verify
        self.assertTrue(client.is_authenticated)
        mock_auth_instance.login.assert_called_once_with("1234567", "password")
    
    @patch('omnivox.client.OmnivoxAuth')
    def test_failed_initialization(self, mock_auth):
        """Test client initialization with failed authentication."""
        # Mock failed authentication
        mock_auth_instance = Mock()
        mock_auth_instance.login.return_value = False
        mock_auth.return_value = mock_auth_instance
        
        # Verify exception is raised
        with self.assertRaises(AuthenticationError):
            OmnivoxClient("invalid", "credentials")
    
    @patch('omnivox.client.OmnivoxAuth')
    @patch('omnivox.client.LeaManager')
    @patch('omnivox.client.MioManager')
    def test_lea_property(self, mock_mio, mock_lea, mock_auth):
        """Test accessing LEA manager."""
        # Mock authentication
        mock_auth_instance = Mock()
        mock_auth_instance.login.return_value = True
        mock_auth_instance.is_authenticated = True
        mock_auth_instance.get_session.return_value = Mock()
        mock_auth.return_value = mock_auth_instance
        
        # Mock LEA manager
        mock_lea_instance = Mock()
        mock_lea.return_value = mock_lea_instance
        
        # Create client and access LEA
        client = OmnivoxClient("1234567", "password")
        lea = client.lea
        
        self.assertEqual(lea, mock_lea_instance)
    
    @patch('omnivox.client.OmnivoxAuth')
    @patch('omnivox.client.LeaManager')
    @patch('omnivox.client.MioManager')
    def test_mio_property(self, mock_mio, mock_lea, mock_auth):
        """Test accessing MIO manager."""
        # Mock authentication
        mock_auth_instance = Mock()
        mock_auth_instance.login.return_value = True
        mock_auth_instance.is_authenticated = True
        mock_auth_instance.get_session.return_value = Mock()
        mock_auth.return_value = mock_auth_instance
        
        # Mock MIO manager
        mock_mio_instance = Mock()
        mock_mio.return_value = mock_mio_instance
        
        # Create client and access MIO
        client = OmnivoxClient("1234567", "password")
        mio = client.mio
        
        self.assertEqual(mio, mock_mio_instance)


if __name__ == '__main__':
    unittest.main()
