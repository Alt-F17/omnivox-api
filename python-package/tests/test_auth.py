"""Tests for authentication module."""

import unittest
from unittest.mock import Mock, patch, MagicMock
from omnivox.auth import OmnivoxAuth
from omnivox.exceptions import AuthenticationError, NetworkError


class TestOmnivoxAuth(unittest.TestCase):
    """Test cases for OmnivoxAuth class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.auth = OmnivoxAuth()
    
    @patch('omnivox.auth.requests.Session')
    def test_successful_login(self, mock_session):
        """Test successful login flow."""
        # Mock responses
        mock_get_response = Mock()
        mock_get_response.text = 'value="6123456789012345678"'
        mock_get_response.raise_for_status = Mock()
        
        mock_post_response = Mock()
        mock_post_response.text = '<div class="headerNavbarLink">Success</div>'
        mock_post_response.raise_for_status = Mock()
        
        # Configure session mock
        mock_session_instance = MagicMock()
        mock_session_instance.get.return_value = mock_get_response
        mock_session_instance.post.return_value = mock_post_response
        mock_session.return_value = mock_session_instance
        
        # Create new auth instance with mocked session
        auth = OmnivoxAuth()
        auth.session = mock_session_instance
        
        # Test login
        result = auth.login("1234567", "password")
        
        self.assertTrue(result)
        self.assertTrue(auth.is_authenticated)
    
    @patch('omnivox.auth.requests.Session')
    def test_failed_login_invalid_credentials(self, mock_session):
        """Test login failure with invalid credentials."""
        # Mock responses
        mock_get_response = Mock()
        mock_get_response.text = 'value="6123456789012345678"'
        mock_get_response.raise_for_status = Mock()
        
        mock_post_response = Mock()
        mock_post_response.text = '<div>Login failed</div>'
        mock_post_response.raise_for_status = Mock()
        
        # Configure session mock
        mock_session_instance = MagicMock()
        mock_session_instance.get.return_value = mock_get_response
        mock_session_instance.post.return_value = mock_post_response
        mock_session.return_value = mock_session_instance
        
        # Create new auth instance with mocked session
        auth = OmnivoxAuth()
        auth.session = mock_session_instance
        
        # Test login
        with self.assertRaises(AuthenticationError):
            auth.login("invalid", "credentials")
        
        self.assertFalse(auth.is_authenticated)
    
    @patch('omnivox.auth.requests.Session')
    def test_failed_login_missing_token(self, mock_session):
        """Test login failure when k token is not found."""
        # Mock responses
        mock_get_response = Mock()
        mock_get_response.text = '<html>No token here</html>'
        mock_get_response.raise_for_status = Mock()
        
        # Configure session mock
        mock_session_instance = MagicMock()
        mock_session_instance.get.return_value = mock_get_response
        mock_session.return_value = mock_session_instance
        
        # Create new auth instance with mocked session
        auth = OmnivoxAuth()
        auth.session = mock_session_instance
        
        # Test login
        with self.assertRaises(AuthenticationError):
            auth.login("1234567", "password")
    
    def test_get_session_when_not_authenticated(self):
        """Test getting session when not authenticated."""
        with self.assertRaises(AuthenticationError):
            self.auth.get_session()


if __name__ == '__main__':
    unittest.main()
