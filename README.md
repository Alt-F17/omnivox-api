# omnivox-api

> **🎯 Goal:** Create a Python pip package for easy Omnivox integration in other applications

## 📦 Project Structure

```
omnivox-api/
├── omnivox-crawler/     # TypeScript crawler (core functionality)
│   ├── src/
│   │   ├── managers/    # LeaManager, MioManager
│   │   ├── modules/     # Scraping logic
│   │   └── types/       # TypeScript interfaces
│   └── build/           # Compiled JavaScript
│
└── archive/             # Old REST/GraphQL implementations (not needed for pip package)
    ├── middleware/      # Express REST API
    ├── graphql-api/     # Apollo GraphQL server
    ├── website/         # SolidJS frontend
    └── api-bindings/    # TypeScript API clients
```

## 🚀 Current Status

The **omnivox-crawler** module is fully functional and can:
- ✅ Authenticate with Omnivox
- ✅ Scrape LEA (courses, documents, grades, schedules)
- ✅ Scrape MIO (messages, send messages, search users)
- ✅ Zero security vulnerabilities
- ✅ Fully typed with TypeScript

## 🎯 Next Steps: Creating Python Package

### Option A: Pure Python Rewrite ⭐ **RECOMMENDED**
Port the TypeScript crawler to pure Python for native pip package distribution.

**Pros:**
- No Node.js dependency for users
- Native Python integration
- Standard pip installation
- Easier maintenance

**Implementation:**
```python
# Future usage:
from omnivox import OmnivoxClient

client = OmnivoxClient("username", "password")
classes = client.lea.get_all_classes()
messages = client.mio.get_messages()
```

### Option B: Python + Node.js Bridge
Wrap the existing TypeScript crawler with Python subprocess calls.

**Pros:**
- Reuse existing, tested TypeScript code
- Faster initial development

**Cons:**
- Users need Node.js installed
- More complex deployment

## 📋 Features To Implement

### LEA (Learning Environment)
- ✅ Get classes with grades
- ✅ Get document summaries
- ❌ Download actual documents (PDFs, etc.)
- ❌ Submit assignments
- ❌ View surveys/quizzes
- ❌ Get full schedule/calendar

### MIO (Internal Messaging)
- ✅ Read messages
- ✅ Send messages
- ❌ Load older messages (pagination)
- ❌ Attachments support
- ❌ Message threading
- ❌ Mark as read/unread

## 🔧 Development Setup

### Working with TypeScript Crawler
```bash
cd omnivox-crawler
npm install
npm run run  # Test the crawler
```

### Building
```bash
cd omnivox-crawler
npx tsc  # Compile TypeScript to JavaScript
```

## 📚 Resources

- Current TypeScript implementation in `omnivox-crawler/`
- Old REST/GraphQL implementations in `archive/` (for reference only)