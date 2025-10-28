# Omnivox API - Python Package

A Python library for interacting with Dawson College's Omnivox platform.

## Features

- 🔐 **Authentication** - Login with student ID and password
- 📚 **LEA (Learning Environment)** - Access courses, documents, grades
- 💬 **MIO (Internal Messaging)** - Read and send messages
- 🐍 **Pythonic API** - Clean, intuitive interface
- 🧪 **Well-tested** - Comprehensive unit tests

## Installation

```bash
pip install -e .
```

## Quick Start

```python
from omnivox import OmnivoxClient

# Initialize and login
client = OmnivoxClient("student_id", "password")

# Get all classes
classes = client.lea.get_all_classes()
for cls in classes:
    print(f"{cls.code}: {cls.title} - {cls.grade}")

# Get messages
messages = client.mio.get_message_previews()
for msg in messages:
    print(f"From {msg.author}: {msg.title}")
```

## API Documentation

### OmnivoxClient

Main client for interacting with Omnivox.

```python
client = OmnivoxClient(username: str, password: str)
```

**Properties:**
- `client.lea` - Access LEA (Learning Environment) manager
- `client.mio` - Access MIO (Internal Messaging) manager
- `client.is_authenticated` - Check if authenticated

### LEA Manager

Access Learning Environment data.

```python
# Get all classes
classes = client.lea.get_all_classes()

# Find specific class
cls = client.lea.get_class(code="420-3A4-DW")
cls = client.lea.get_class(teacher="John Doe")
cls = client.lea.get_class(name="Web Programming")

# Get document summary
summaries = client.lea.get_class_document_summary()

# Get documents for a class
categories = client.lea.get_class_documents_by_href(summary.href)
for category in categories:
    print(f"{category.name}:")
    for doc in category.documents:
        print(f"  - {doc.name} (posted: {doc.posted})")
```

### MIO Manager

Access Internal Messaging data.

```python
# Get message previews
previews = client.mio.get_message_previews()

# Get full message
message = client.mio.get_message_by_id(preview.id)
print(f"From: {message.author}")
print(f"Subject: {message.title}")
print(f"Content: {message.content}")

# Search users (not yet implemented)
# users = client.mio.search_users("John")

# Send message (not yet implemented)
# client.mio.send_message(recipients, "Subject", "Message body")
```

## Development

### Setup

```bash
# Install in development mode with dev dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=omnivox tests/

# Run specific test file
python -m pytest tests/test_auth.py
```

### Code Style

```bash
# Format code
black omnivox tests

# Check code style
flake8 omnivox tests

# Type checking
mypy omnivox
```

## Project Structure

```
python-package/
├── omnivox/                    # Main package
│   ├── __init__.py            # Package exports
│   ├── client.py              # OmnivoxClient
│   ├── auth.py                # Authentication
│   ├── exceptions.py          # Custom exceptions
│   ├── utils.py               # Utility functions
│   ├── lea/                   # LEA module
│   │   ├── __init__.py
│   │   ├── manager.py         # LeaManager
│   │   └── models.py          # Data classes
│   └── mio/                   # MIO module
│       ├── __init__.py
│       ├── manager.py         # MioManager
│       └── models.py          # Data classes
├── tests/                     # Test suite
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_client.py
│   ├── test_lea.py
│   ├── test_mio.py
│   └── test_utils.py
├── setup.py                   # Package configuration
├── requirements.txt           # Dependencies
└── README.md                  # This file
```

## Implementation Status

### ✅ Completed
- [x] Authentication (login)
- [x] LEA: Get all classes
- [x] LEA: Get class documents
- [x] LEA: Get document summaries
- [x] MIO: Get message previews
- [x] MIO: Get message by ID

### 🚧 In Progress
- [ ] MIO: Search users
- [ ] MIO: Send messages

### 📋 Planned
- [ ] Error handling improvements
- [ ] Retry logic for network failures
- [ ] Response caching
- [ ] Async support (asyncio)
- [ ] CLI tool

## Dependencies

- **requests** - HTTP client
- **beautifulsoup4** - HTML parsing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run tests and ensure they pass
6. Submit a pull request

## License

MIT License - see LICENSE file for details

## Disclaimer

This is an unofficial API client. Use at your own risk. The Omnivox platform is owned by Skytech Communications.

## Credits

Based on the TypeScript implementation in `omnivox-crawler/`.
