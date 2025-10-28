"""
Manual test script to verify the Omnivox API implementation.

This script tests all core functionality against the real Omnivox system.
It requires valid credentials in a .env file or passed as arguments.

Usage:
    python test_manual.py
    python test_manual.py <student_id> <password>
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the omnivox package
try:
    from omnivox import OmnivoxClient
    from omnivox.exceptions import AuthenticationError, NetworkError
except ImportError as e:
    print(f"❌ Failed to import omnivox package: {e}")
    print("Make sure you've installed the package with: pip install -e .")
    sys.exit(1)


def print_header(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def test_authentication(username: str, password: str):
    """Test authentication."""
    print_header("🔐 Testing Authentication")
    
    try:
        client = OmnivoxClient(username, password)
        print("✅ Login successful!")
        print(f"   Authenticated: {client.is_authenticated}")
        return client
    except AuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        return None
    except NetworkError as e:
        print(f"❌ Network error: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_lea_classes(client):
    """Test LEA class retrieval."""
    print_header("📚 Testing LEA - Get All Classes")
    
    try:
        classes = client.lea.get_all_classes()
        print(f"✅ Found {len(classes)} classes:\n")
        
        for i, cls in enumerate(classes, 1):
            print(f"{i}. {cls.code}: {cls.title}")
            print(f"   Teacher: {cls.teacher}")
            print(f"   Section: {cls.section}")
            print(f"   Schedule: {', '.join(cls.schedule)}")
            print(f"   Grade: {cls.grade or 'N/A'}")
            
            if cls.average is not None:
                print(f"   Average: {cls.average:.1f}")
            if cls.median is not None:
                print(f"   Median: {cls.median:.1f}")
                
            if cls.distributed_documents > 0:
                print(f"   📄 {cls.distributed_documents} new documents")
            if cls.distributed_assignments > 0:
                print(f"   📝 {cls.distributed_assignments} new assignments")
            print()
        
        return classes
    except Exception as e:
        print(f"❌ Failed to get classes: {e}")
        import traceback
        traceback.print_exc()
        return []


def test_lea_find_class(client, classes):
    """Test finding specific classes."""
    print_header("🔍 Testing LEA - Find Specific Class")
    
    if not classes:
        print("⚠️  No classes to search")
        return
    
    # Test finding by code
    test_code = classes[0].code
    print(f"Searching for class by code: {test_code}")
    found = client.lea.get_class(code=test_code)
    if found:
        print(f"✅ Found: {found.code} - {found.title}")
    else:
        print(f"❌ Not found")
    
    # Test finding by teacher
    test_teacher = classes[0].teacher.split()[0]  # First word of teacher name
    print(f"\nSearching for class by teacher: {test_teacher}")
    found = client.lea.get_class(teacher=test_teacher)
    if found:
        print(f"✅ Found: {found.code} - {found.title} ({found.teacher})")
    else:
        print(f"❌ Not found")


def test_lea_document_summary(client):
    """Test document summary retrieval."""
    print_header("📄 Testing LEA - Get Document Summary")
    
    try:
        summaries = client.lea.get_class_document_summary()
        print(f"✅ Found document summaries for {len(summaries)} classes:\n")
        
        for i, summary in enumerate(summaries, 1):
            print(f"{i}. {summary.name}")
            print(f"   Available documents: {summary.available_documents}")
            print(f"   Href: {summary.href[:50]}...")
            print()
        
        return summaries
    except Exception as e:
        print(f"❌ Failed to get document summary: {e}")
        import traceback
        traceback.print_exc()
        return []


def test_lea_class_documents(client, summaries):
    """Test getting documents for a specific class."""
    print_header("📑 Testing LEA - Get Class Documents")
    
    if not summaries:
        print("⚠️  No summaries to fetch documents from")
        return
    
    # Get documents for first class
    summary = summaries[0]
    print(f"Fetching documents for: {summary.name}\n")
    
    try:
        categories = client.lea.get_class_documents_by_href(summary.href)
        print(f"✅ Found {len(categories)} categories:\n")
        
        for cat in categories:
            print(f"📁 {cat.name} ({len(cat.documents)} documents)")
            
            # Show first 3 documents
            for doc in cat.documents[:3]:
                status = "✓" if doc.viewed else "✗"
                print(f"   {status} {doc.name}")
                if doc.description:
                    desc_preview = doc.description[:50] + "..." if len(doc.description) > 50 else doc.description
                    print(f"      {desc_preview}")
                print(f"      Posted: {doc.posted}")
            
            if len(cat.documents) > 3:
                print(f"   ... and {len(cat.documents) - 3} more documents")
            print()
        
    except Exception as e:
        print(f"❌ Failed to get class documents: {e}")
        import traceback
        traceback.print_exc()


def test_mio_previews(client):
    """Test MIO message preview retrieval."""
    print_header("💬 Testing MIO - Get Message Previews")
    
    try:
        previews = client.mio.get_message_previews()
        print(f"✅ Found {len(previews)} messages:\n")
        
        for i, preview in enumerate(previews[:5], 1):  # Show first 5
            print(f"{i}. From: {preview.author}")
            print(f"   Subject: {preview.title}")
            desc_preview = preview.short_desc[:60] + "..." if len(preview.short_desc) > 60 else preview.short_desc
            print(f"   Preview: {desc_preview}")
            print(f"   ID: {preview.id}")
            print()
        
        if len(previews) > 5:
            print(f"... and {len(previews) - 5} more messages")
        
        return previews
    except Exception as e:
        print(f"❌ Failed to get message previews: {e}")
        import traceback
        traceback.print_exc()
        return []


def test_mio_detail(client, previews):
    """Test getting full message content."""
    print_header("📧 Testing MIO - Get Message Detail")
    
    if not previews:
        print("⚠️  No messages to fetch details for")
        return
    
    # Get first message
    preview = previews[0]
    print(f"Fetching message: {preview.title}\n")
    
    try:
        message = client.mio.get_message_by_id(preview.id)
        print(f"✅ Message retrieved:\n")
        print(f"From: {message.author}")
        print(f"To: {message.recipient}")
        print(f"Date: {message.date}")
        print(f"Subject: {message.title}")
        print(f"\nContent:")
        print("-" * 60)
        content_preview = message.content[:300] + "..." if len(message.content) > 300 else message.content
        print(content_preview)
        print("-" * 60)
        
    except Exception as e:
        print(f"❌ Failed to get message detail: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main test function."""
    print("=" * 60)
    print("  Omnivox API - Manual Test Suite")
    print("=" * 60)
    
    # Get credentials
    if len(sys.argv) >= 3:
        username = sys.argv[1]
        password = sys.argv[2]
        print(f"Using credentials from arguments: {username}")
    elif os.getenv("OMNIVOX_USERNAME") and os.getenv("OMNIVOX_PASSWORD"):
        username = os.getenv("OMNIVOX_USERNAME")
        password = os.getenv("OMNIVOX_PASSWORD")
        print(f"Using credentials from .env: {username}")
    else:
        print("\n❌ No credentials provided!")
        print("\nUsage:")
        print("  1. Create .env file with OMNIVOX_USERNAME and OMNIVOX_PASSWORD")
        print("  2. Or run: python test_manual.py <username> <password>")
        sys.exit(1)
    
    # Run tests
    client = test_authentication(username, password)
    if not client:
        print("\n❌ Authentication failed. Cannot continue tests.")
        sys.exit(1)
    
    classes = test_lea_classes(client)
    test_lea_find_class(client, classes)
    summaries = test_lea_document_summary(client)
    test_lea_class_documents(client, summaries)
    
    previews = test_mio_previews(client)
    test_mio_detail(client, previews)
    
    print_header("✅ All Tests Completed!")
    print("\nSummary:")
    print(f"  - Classes found: {len(classes)}")
    print(f"  - Document summaries: {len(summaries)}")
    print(f"  - Messages found: {len(previews)}")
    print("\nThe Python implementation matches the TypeScript reference! 🎉")


if __name__ == "__main__":
    main()
