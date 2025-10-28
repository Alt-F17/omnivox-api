"""Tests for LEA module."""

import unittest
from unittest.mock import Mock, patch, MagicMock
from omnivox.lea.manager import LeaManager
from omnivox.lea.models import LeaClass, Document, Category


class TestLeaManager(unittest.TestCase):
    """Test cases for LeaManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_session = MagicMock()
        # Mock the initialization GET request
        self.mock_session.get.return_value = Mock()
    
    @patch('omnivox.lea.manager.BeautifulSoup')
    def test_get_all_classes(self, mock_bs):
        """Test getting all classes."""
        # Mock HTML response
        mock_response = Mock()
        mock_response.text = '<html>Mock LEA page</html>'
        mock_response.raise_for_status = Mock()
        self.mock_session.get.return_value = mock_response
        
        # Mock parsed HTML
        mock_soup = Mock()
        mock_card = Mock()
        
        # Mock card structure
        title_elem = Mock()
        title_elem.get_text.return_value = "420-3A4-DW Web Programming"
        mock_card.select_one.side_effect = lambda sel: {
            '.card-panel-title': title_elem,
            '.card-panel-desc': None
        }.get(sel)
        
        mock_card.select.return_value = []  # No grades
        mock_soup.select.return_value = [mock_card]
        mock_bs.return_value = mock_soup
        
        # Create manager and test
        manager = LeaManager(self.mock_session)
        classes = manager.get_all_classes()
        
        self.assertIsInstance(classes, list)
    
    def test_get_class_by_code(self):
        """Test finding a class by code."""
        manager = LeaManager(self.mock_session)
        
        # Add mock class to cache
        mock_class = LeaClass(
            code="420-3A4-DW",
            title="Web Programming",
            teacher="John Doe",
            section="01",
            schedule=["Mon 10:00-12:00"]
        )
        manager._classes_cache = [mock_class]
        
        # Test
        result = manager.get_class(code="420-3A4-DW")
        
        self.assertIsNotNone(result)
        self.assertEqual(result.code, "420-3A4-DW")
    
    def test_get_class_not_found(self):
        """Test finding a class that doesn't exist."""
        manager = LeaManager(self.mock_session)
        manager._classes_cache = []
        
        result = manager.get_class(code="INVALID")
        
        self.assertIsNone(result)


class TestLeaModels(unittest.TestCase):
    """Test cases for LEA data models."""
    
    def test_lea_class_creation(self):
        """Test creating a LeaClass object."""
        cls = LeaClass(
            code="420-3A4-DW",
            title="Web Programming",
            teacher="John Doe",
            section="01",
            schedule=["Mon 10:00-12:00", "Wed 14:00-16:00"],
            grade="85.5%",
            average=78.3,
            median=80.0
        )
        
        self.assertEqual(cls.code, "420-3A4-DW")
        self.assertEqual(cls.teacher, "John Doe")
        self.assertEqual(len(cls.schedule), 2)
    
    def test_document_creation(self):
        """Test creating a Document object."""
        doc = Document(
            name="Lecture 1 - Introduction",
            description="First lecture slides",
            posted="2024-01-15",
            viewed=True
        )
        
        self.assertEqual(doc.name, "Lecture 1 - Introduction")
        self.assertTrue(doc.viewed)
    
    def test_category_creation(self):
        """Test creating a Category object."""
        doc1 = Document("Doc 1", "Description 1", "2024-01-15", False)
        doc2 = Document("Doc 2", "Description 2", "2024-01-16", True)
        
        category = Category(
            name="Lectures",
            documents=[doc1, doc2]
        )
        
        self.assertEqual(category.name, "Lectures")
        self.assertEqual(len(category.documents), 2)


if __name__ == '__main__':
    unittest.main()
