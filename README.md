# 🔐 Hash Function Tool

A professional web-based cryptographic hash generator built with Python Flask. This cybersecurity project demonstrates practical implementation of hash algorithms and web application security principles.

![Hash Function Tool](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🚀 Features

### Core Functionality
- **Multiple Hash Algorithms**: MD5, SHA-1, SHA-256, SHA-512
- **Text Hashing**: Generate hashes for any text input
- **File Hashing**: Upload and hash files of any type
- **Hash Comparison**: Compare generated hashes with existing ones
- **History Tracking**: SQLite database stores all hash operations
- **RESTful API**: Programmatic access via JSON API

### User Interface
- **Modern Web Interface**: Clean, responsive design
- **Real-time Feedback**: Copy to clipboard functionality
- **Filtering & Search**: Filter history by algorithm, type, or content
- **Statistics Dashboard**: Visual breakdown of hash operations
- **Mobile Responsive**: Works on all device sizes

### Security Features
- **Input Validation**: Secure file upload handling
- **Error Handling**: Comprehensive error management
- **Data Integrity**: SQLite database with proper schemas
- **Clean Architecture**: Separation of concerns between frontend/backend

## 🛠️ Technology Stack

- **Backend**: Python 3.8+, Flask 2.3.3
- **Database**: SQLite 3
- **Frontend**: HTML5, CSS3, JavaScript (ES6)
- **Styling**: Modern CSS with gradients and animations
- **Architecture**: MVC pattern with RESTful API

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Modern web browser

## 🔧 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/hash-function-tool.git
cd hash-function-tool
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Initialize Database
```bash
python database.py
```

### 4. Run the Application
```bash
python app.py
```

### 5. Access the Application
Open your browser and navigate to: `http://127.0.0.1:5000`

## 🎯 Usage

### Web Interface

1. **Hash Text**:
   - Navigate to the homepage
   - Enter text in the "Hash Text" section
   - Click "Generate Hash" to see MD5, SHA-1, SHA-256, and SHA-512 hashes

2. **Hash Files**:
   - Use the "Hash File" section
   - Upload any file type
   - View all hash algorithms for the uploaded file

3. **View History**:
   - Click "History" in the navigation
   - Filter by algorithm, input type, or search content
   - Copy any hash with one click

4. **Compare Hashes**:
   - On the results page, use the comparison tool
   - Paste an existing hash to verify integrity

### API Usage

The application provides a RESTful API for programmatic access:

```bash
# Hash text via API
curl -X POST http://127.0.0.1:5000/api/hash \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello World"}'
```

**Response:**
```json
{
  "input": "Hello World",
  "hashes": {
    "md5": "b10a8db164e0754105b7a99be72e3fe5",
    "sha1": "0a4d55a8d778e5022fab701977c5d840bbc486d0",
    "sha256": "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e",
    "sha512": "374d794a95cdcfd8b35993185fef9ba368f160d8daf432d08ba9f1ed1e5abe6cc69291e0fa2fe0006a52570ef18c19def4e617c33ce52ef0a6e5fbe318cb0387"
  }
}
```

## 📁 Project Structure

```
hash-function-tool/
├── app.py                 # Main Flask application
├── database.py            # SQLite database operations
├── requirements.txt       # Python dependencies
├── hash_results.db       # SQLite database file
├── README.md             # Project documentation
├── templates/            # HTML templates
│   ├── index.html        # Homepage
│   ├── results.html      # Hash results page
│   └── history.html      # History page
└── static/              # Static files
    └── style.css        # CSS styling
```

## 🔍 Code Explanation

### Flask Application (`app.py`)
The main application uses Flask routes to handle different endpoints:
- `/` - Homepage with hash forms
- `/hash_text` - Process text hashing requests
- `/hash_file` - Handle file upload and hashing
- `/history` - Display hash history
- `/api/hash` - RESTful API endpoint

### Database Operations (`database.py`)
SQLite integration with Python functions:
- `init_db()` - Create database tables
- `save_hash_result()` - Store hash operations
- `get_hash_history()` - Retrieve historical data
- `get_database_stats()` - Generate usage statistics

### Frontend (`templates/` and `static/`)
Modern web interface with:
- Responsive CSS Grid/Flexbox layouts
- JavaScript for interactive features
- Copy-to-clipboard functionality
- Real-time filtering and search

## 🛡️ Security Considerations

- **Input Sanitization**: All user inputs are properly validated
- **File Upload Security**: Secure file handling without execution
- **SQL Injection Prevention**: Parameterized queries used throughout
- **Error Handling**: Graceful error management prevents information disclosure
- **Hash Algorithm Selection**: Multiple algorithms for different security needs

## 📊 Hash Algorithm Information

| Algorithm | Bit Length | Security Status | Use Case |
|-----------|------------|-----------------|----------|
| MD5       | 128        | ⚠️ Deprecated   | Checksums only |
| SHA-1     | 160        | ⚠️ Deprecated   | Legacy systems |
| SHA-256   | 256        | ✅ Secure       | Current standard |
| SHA-512   | 512        | ✅ Secure       | High security |

## 🎯 Cybersecurity Learning Objectives

This project demonstrates:

1. **Cryptographic Hash Functions**: Practical implementation of industry-standard algorithms
2. **Web Application Security**: Secure coding practices in Python/Flask
3. **Database Security**: SQLite integration with proper data handling
4. **Input Validation**: Preventing common web vulnerabilities
5. **API Development**: RESTful service design and implementation
6. **File Integrity**: Using hashes for file verification and integrity checking

## 🚀 Deployment Options

### Local Development
```bash
python app.py
# Access at http://127.0.0.1:5000
```

### Production Deployment
For production deployment, consider:
- **Heroku**: Easy cloud deployment
- **AWS/Azure**: Scalable cloud platforms
- **Docker**: Containerized deployment
- **WSGI Server**: Use Gunicorn instead of Flask dev server

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎓 Educational Use

This project is designed for:
- **Cybersecurity Students**: Understanding hash functions and web security
- **Portfolio Development**: Demonstrating full-stack development skills
- **Interview Preparation**: Discussing security concepts and implementation
- **Learning Python/Flask**: Practical web application development

## 📧 Contact

**Project Developer**: [Zaka shaikh]
- **Email**: [shaikhzakaurrehman@gmail.com]


## 🏆 Resume Highlights

**Key Skills Demonstrated:**
- Python programming and Flask framework
- Database design and SQLite integration
- Frontend development (HTML/CSS/JavaScript)
- Cybersecurity principles and cryptographic implementations
- RESTful API design and development
- Version control with Git/GitHub

---

⭐ **Star this repository if you found it helpful!**

*Built with ❤️ for cybersecurity education and professional development*
