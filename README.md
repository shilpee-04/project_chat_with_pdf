# Chat with PDF - Advanced RAG System

A Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and chat with them using natural language. The system supports both multi-turn conversations and single-turn deep research queries with proper source citations.

## Features

- **PDF Upload & Processing**: Upload single or multiple PDF files (supports 500+ page documents)
- **Multi-turn Conversations**: Maintain context across multiple questions
- **Deep Research Mode**: Comprehensive single-turn analysis with detailed responses
- **Source Citations**: All answers include page number references from uploaded PDFs
- **Local Deployment**: Runs entirely on your local machine
- **Modern UI**: Clean web interface with drag-and-drop file upload

## Prerequisites

- Python 3.12 or higher
- Git
- A Groq API key (free tier available)

## Installation

### 1. Clone the Repository

```bash
git clone <your-github-repo-url>
cd chat_with_pdf
```

### 2. Install Python Dependencies

```bash
pip install fastapi uvicorn python-multipart jinja2 langchain langchain-community faiss-cpu pypdf python-dotenv groq InstructorEmbedding sentence-transformers torch
```

**Note for Windows users**: If you encounter DLL errors with PyTorch, you may need to:
- Install Microsoft Visual C++ 2015-2022 Redistributable
- Or download `libomp140.x86_64.dll` and place it in `C:\Windows\System32\`

### 3. Set Up Environment Variables

Create a `.env` file in the `backend` directory:

```bash
cd backend
touch .env  # Linux/Mac
# or create .env file manually on Windows
```

Add your Groq API key to the `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
```

**To get a Groq API key:**
1. Visit [console.groq.com](https://console.groq.com)
2. Sign up/Login to your account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (starts with `gsk_`)

### 4. Create Required Directories

```bash
mkdir vector_stores  # This will store processed PDF embeddings
```

## Running the Application

### 1. Start the Backend Server

From the `backend` directory:

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [XXXX] using StatReload
INFO:     Started server process [XXXX]
INFO:     Application startup complete.
```

### 2. Access the Application

Open your web browser and navigate to:
```
http://localhost:8000
```

## Quick Demo Commands

### Web Interface Demo

1. **Upload PDF**: Drag and drop or select PDF files using the upload interface
2. **Process Documents**: Click "Process Documents" button
3. **Start Chatting**: Ask questions about your uploaded PDFs
4. **Switch Modes**: Toggle between "Multi-turn Conversation" and "Deep Research Mode"

### API Testing with Curl

**Upload a PDF:**
```bash
curl -X POST "http://localhost:8000/api/v1/pdf/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@your_document.pdf"
```

**Chat with uploaded PDF:**
```bash
curl -X POST "http://localhost:8000/api/v1/chat/chat" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the main topic of this document?",
    "store_ids": ["your_store_id_from_upload_response"],
    "mode": "multi-turn"
  }'
```

### Swagger UI Testing

Visit `http://localhost:8000/docs` for interactive API documentation and testing.

## Project Structure

```
chat_with_pdf/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI application entry point
│   │   ├── api/routes/
│   │   │   ├── pdf_routes.py       # PDF upload endpoints
│   │   │   └── chat_routes.py      # Chat endpoints
│   │   └── services/
│   │       ├── pdf_processor.py    # PDF text extraction & vectorization
│   │       ├── chat_service.py     # Chat orchestration
│   │       └── llm_service.py      # LLM integration (Groq)
│   ├── .env                        # Environment variables
│   └── vector_stores/              # Generated vector databases
├── frontend/
│   ├── templates/
│   │   └── index.html              # Main web interface
│   └── static/
│       ├── css/style.css           # Styling
│       └── js/main.js              # Frontend logic
└── README.md
```

## Usage Examples

### Multi-turn Conversation
```
User: "What are the main findings in this research paper?"
Assistant: "Based on the document [Page 3], the main findings include..."

User: "Can you elaborate on the methodology?"
Assistant: "The methodology described on [Page 5-7] involves..."
```

### Deep Research Mode
```
User: "Provide a comprehensive analysis of the business strategy outlined in this document"
Assistant: "Based on comprehensive analysis of the document:

1. Strategic Overview [Page 2]: ...
2. Market Analysis [Page 8-12]: ...
3. Implementation Timeline [Page 15]: ...
..."
```

## Troubleshooting

### Common Issues

**Error: "No module named 'app'"**
- Make sure you're running `uvicorn app.main:app` from the `backend` directory

**Error: "GROQ_API_KEY not found"**
- Ensure you've created the `.env` file in the `backend` directory
- Verify your API key is correctly set in the `.env` file

**Error: "PyTorch DLL load failed" (Windows)**
- Install Microsoft Visual C++ 2015-2022 Redistributable
- Or manually download and install `libomp140.x86_64.dll`

**Error: "Failed to process PDF"**
- Ensure your PDF contains readable text (not just images)
- Try with a different PDF file
- Check that the PDF file is not corrupted

**Slow processing on first run**
- The first run downloads the embedding model (~1.3GB)
- Subsequent runs will be much faster

### Performance Notes

- **First-time setup**: The initial run will download the INSTRUCTOR embedding model
- **Memory usage**: Large PDFs (500+ pages) may require 4GB+ RAM
- **Processing time**: Expect 30-60 seconds for large PDF processing

## System Requirements

- **RAM**: Minimum 4GB, 8GB recommended for large documents
- **Storage**: 2GB free space for models and vector stores
- **Network**: Internet connection required for initial model download and LLM API calls

## API Documentation

Once running, visit `http://localhost:8000/docs` for complete API documentation with interactive testing capabilities.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is available for educational and personal use.

---

**Need help?** Check the troubleshooting section above or create an issue in the GitHub repository.
