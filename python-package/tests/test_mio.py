"""Tests for MIO module."""

import unittest
from unittest.mock import Mock, patch, MagicMock
from omnivox.mio.manager import MioManager
from omnivox.mio.models import Mio, MioPreview, SearchUser


class TestMioManager(unittest.TestCase):
    """Test cases for MioManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_session = MagicMock()
        # Mock the initialization GET request
        self.mock_session.get.return_value = Mock()
    
    @patch('omnivox.mio.manager.BeautifulSoup')
    def test_get_message_previews(self, mock_bs):
        """Test getting message previews."""
        # Mock HTML response with message data
        mock_response = Mock()
        mock_response.text = 'chk12345678-1234-1234-1234-123456789abc'
        mock_response.raise_for_status = Mock()
        self.mock_session.get.return_value = mock_response
        
        # Mock parsed HTML
        mock_soup = Mock()
        
        # Mock message elements
        name_elem = Mock()
        name_elem.get_text.return_value = "John Doe"
        
        title_elem = Mock()
        title_elem.get_text.return_value = "Test Message"
        
        desc_elem = Mock()
        desc_elem.get_text.return_value = "This is a test message"
        
        mock_soup.select.side_effect = lambda sel: {
            '.name': [name_elem],
            '.lsTdTitle > div > em': [title_elem],
            '.lsTdTitle > div': [desc_elem]
        }.get(sel, [])
        
        mock_bs.return_value = mock_soup
        
        # Create manager and test
        manager = MioManager(self.mock_session)
        previews = manager.get_message_previews()
        
        self.assertIsInstance(previews, list)
    
    @patch('omnivox.mio.manager.BeautifulSoup')
    def test_get_message_by_id(self, mock_bs):
        """Test getting a message by ID."""
        # Mock HTML response
        mock_response = Mock()
        mock_response.text = '<html>Message content</html>'
        mock_response.raise_for_status = Mock()
        self.mock_session.get.return_value = mock_response
        
        # Mock parsed HTML
        mock_soup = Mock()
        
        content_wrapper = Mock()
        content_wrapper.get_text.return_value = "Message body"
        
        from_elem = Mock()
        from_elem.get_text.return_value = "John Doe"
        
        to_elem = Mock()
        to_elem.get_text.return_value = "Jane Smith"
        
        title_elem = Mock()
        title_elem.get_text.return_value = "Test Message"
        
        date_elem = Mock()
        date_elem.get_text.return_value = "2024-01-15"
        
        mock_soup.select_one.side_effect = lambda sel: {
            '#contenuWrapper': content_wrapper,
            '.cDe': from_elem,
            '#tdACont': to_elem,
            '.cSujet': title_elem,
            '.cDate': date_elem
        }.get(sel)
        
        mock_bs.return_value = mock_soup
        
        # Create manager and test
        manager = MioManager(self.mock_session)
        message = manager.get_message_by_id("test-id-123")
        
        self.assertIsInstance(message, Mio)
        self.assertEqual(message.id, "test-id-123")


class TestMioModels(unittest.TestCase):
    """Test cases for MIO data models."""
    
    def test_mio_preview_creation(self):
        """Test creating a MioPreview object."""
        preview = MioPreview(
            id="12345678-1234-1234-1234-123456789abc",
            author="John Doe",
            title="Test Message",
            short_desc="This is a preview"
        )
        
        self.assertEqual(preview.author, "John Doe")
        self.assertEqual(preview.title, "Test Message")
    
    def test_mio_creation(self):
        """Test creating a Mio object."""
        mio = Mio(
            id="12345678-1234-1234-1234-123456789abc",
            author="John Doe",
            recipient="Jane Smith",
            title="Test Message",
            date="2024-01-15",
            content="This is the full message content."
        )
        
        self.assertEqual(mio.author, "John Doe")
        self.assertEqual(mio.recipient, "Jane Smith")
        self.assertEqual(mio.date, "2024-01-15")
    
    def test_search_user_creation(self):
        """Test creating a SearchUser object."""
        user = SearchUser(
            numero="1234567",
            titre="John Doe",
            username="jdoe",
            type_item_selectionne=3,
            type_item_string="Etudiant"
        )
        
        self.assertEqual(user.numero, "1234567")
        self.assertEqual(user.titre, "John Doe")
        self.assertEqual(user.type_item_string, "Etudiant")
    
    def test_search_user_from_api_response(self):
        """Test creating SearchUser from API response."""
        api_data = {
            "Numero": "1234567",
            "Titre": "John Doe",
            "Username": "jdoe",
            "TypeItemSelectionne": 3,
            "TypeItemString": "Etudiant",
            "NbEtudiants": 0
        }
        
        user = SearchUser.from_api_response(api_data)
        
        self.assertEqual(user.numero, "1234567")
        self.assertEqual(user.titre, "John Doe")


if __name__ == '__main__':
    unittest.main()
