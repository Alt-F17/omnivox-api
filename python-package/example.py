"""
Example usage of the Omnivox API.

This script demonstrates how to use the library to:
1. Authenticate with Omnivox
2. Get all classes and their information
3. Get documents for each class
4. Get messages from MIO
"""

from omnivox import OmnivoxClient
from omnivox.exceptions import AuthenticationError, NetworkError
import sys


def main():
    """Main example function."""
    
    # Get credentials (in real app, use environment variables or secure input)
    print("Omnivox API Example")
    print("=" * 50)
    
    if len(sys.argv) > 2:
        username = sys.argv[1]
        password = sys.argv[2]
    else:
        username = input("Student ID: ")
        password = input("Password: ")
    
    try:
        # Initialize client and login
        print("\n🔐 Logging in...")
        client = OmnivoxClient(username, password)
        print("✅ Successfully logged in!")
        
        # Get all classes
        print("\n📚 Fetching classes...")
        classes = client.lea.get_all_classes()
        print(f"✅ Found {len(classes)} classes:\n")
        
        for cls in classes:
            print(f"  📖 {cls.code}: {cls.title}")
            print(f"     Teacher: {cls.teacher}")
            print(f"     Grade: {cls.grade or 'N/A'}")
            if cls.distributed_documents > 0:
                print(f"     📄 {cls.distributed_documents} new documents")
            if cls.distributed_assignments > 0:
                print(f"     📝 {cls.distributed_assignments} new assignments")
            print()
        
        # Get document summaries
        print("\n📄 Fetching document summaries...")
        summaries = client.lea.get_class_document_summary()
        
        if summaries:
            print(f"✅ Found document summaries for {len(summaries)} classes:\n")
            
            for summary in summaries:
                print(f"  📚 {summary.name}")
                print(f"     Available documents: {summary.available_documents}")
                
                # Get documents for first class as example
                if summary == summaries[0]:
                    print(f"\n     Fetching documents...")
                    categories = client.lea.get_class_documents_by_href(summary.href)
                    
                    for category in categories:
                        print(f"\n     Category: {category.name}")
                        for doc in category.documents[:3]:  # Show first 3 documents
                            status = "✓" if doc.viewed else "✗"
                            print(f"       {status} {doc.name}")
                            print(f"         Posted: {doc.posted}")
                        if len(category.documents) > 3:
                            print(f"       ... and {len(category.documents) - 3} more")
                print()
        
        # Get messages
        print("\n💬 Fetching messages...")
        previews = client.mio.get_message_previews()
        print(f"✅ Found {len(previews)} messages:\n")
        
        for preview in previews[:5]:  # Show first 5 messages
            print(f"  📧 From: {preview.author}")
            print(f"     Subject: {preview.title}")
            print(f"     Preview: {preview.short_desc[:60]}...")
            print()
        
        if len(previews) > 5:
            print(f"  ... and {len(previews) - 5} more messages")
        
        # Get full content of first message
        if previews:
            print(f"\n📧 Fetching first message content...")
            message = client.mio.get_message_by_id(previews[0].id)
            print(f"\n  From: {message.author}")
            print(f"  To: {message.recipient}")
            print(f"  Date: {message.date}")
            print(f"  Subject: {message.title}")
            print(f"  Content:\n  {message.content[:200]}...")
        
        print("\n" + "=" * 50)
        print("✅ Example completed successfully!")
        
    except AuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        sys.exit(1)
    
    except NetworkError as e:
        print(f"❌ Network error: {e}")
        sys.exit(1)
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
