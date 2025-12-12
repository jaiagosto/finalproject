# Advanced Calculator Application - IS601855 Final Project

A full-stack web application featuring a calculator with user authentication, calculation history tracking, and analytics dashboard. Built with FastAPI, PostgreSQL, Redis, and modern web technologies.

**Student:** Jailene Agosto  
**Course:** IS601855 Python for Web API Development  
**Semester:** Fall 2025 
**Institution:** NJIT

## 🚀 Features

### Core Functionality (BREAD Operations)
- ✅ **Browse**: View all calculations with pagination
- ✅ **Read**: Get individual calculation details  
- ✅ **Edit**: Update existing calculations
- ✅ **Add**: Create new calculations
- ✅ **Delete**: Remove calculations

### Advanced Features (Final Project)
- 📊 **Calculation History**: Track all calculations with timestamps
- 📈 **Analytics Dashboard**: 
  - Total calculations count
  - Most used operation
  - Average result
  - Operations breakdown with percentages
- 🔐 **Secure Authentication**: 
  - JWT token-based auth
  - Password hashing with bcrypt
  - Token blacklisting with Redis
- 👤 **User Profile Management**:
  - Update username and email
  - Change password
  - Account deletion
- 🧮 **Multiple Operations**:
  - Addition
  - Subtraction
  - Multiplication
  - Division
  - Power (exponentiation)
  - Modulus

### Security Features
- JWT authentication with token expiration
- Password hashing using bcrypt
- Token blacklisting for logout
- SQL injection protection via SQLAlchemy
- Input validation with Pydantic
- CORS configuration

## 🏗️ Architecture

### Backend
- **Framework**: FastAPI 0.115.5
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **ORM**: SQLAlchemy 2.0
- **Validation**: Pydantic 2.10
- **Authentication**: python-jose with JWT

### Frontend
- **HTML5** with semantic markup
- **CSS3** with modern styling (no frameworks)
- **Vanilla JavaScript** (no dependencies)
- **Responsive design** for mobile/desktop

### DevOps
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions
- **Security Scanning**: Trivy
- **Testing**: pytest, pytest-cov, Playwright

## 📦 Project Structure
```
finalproject/
├── app/
│   ├── core/
│   │   ├── config.py           # Configuration settings
│   │   ├── database.py         # Database connection
│   │   └── security.py         # Authentication & security
│   ├── models/
│   │   ├── user.py            # User model
│   │   └── calculation.py     # Calculation model
│   ├── schemas/
│   │   ├── user.py            # User Pydantic schemas
│   │   ├── calculation.py     # Calculation schemas
│   │   └── analytics.py       # Analytics schemas
│   ├── routes/
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── users.py           # User profile endpoints
│   │   ├── calculations.py    # Calculation BREAD endpoints
│   │   └── analytics.py       # History & analytics endpoints
│   ├── services/
│   │   ├── calculator.py      # Calculator business logic
│   │   └── analytics.py       # Analytics business logic
│   ├── static/
│   │   ├── css/style.css      # Application styles
│   │   └── js/app.js          # Frontend JavaScript
│   └── templates/
│       └── index.html         # Main HTML template
├── tests/
│   ├── unit/                  # Unit tests
│   ├── integration/           # Integration tests
│   └── e2e/                   # End-to-end tests
├── .github/
│   └── workflows/
│       └── ci-cd.yml         # CI/CD pipeline
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker image definition
├── docker-compose.yml         # Multi-container setup
└── README.md                  # This file
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Git

### Local Development Setup

1. **Clone the repository**
```bash
git clone https://github.com/jaiagosto/finalproject.git
cd finalproject
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Start services with Docker Compose**
```bash
docker-compose up -d
```

6. **Access the application**
- Application: http://localhost:8000
- API Documentation: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

### Using Docker Only
```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🧪 Testing

### Run All Tests
```bash
pytest
```

### Run Specific Test Types
```bash
# Unit tests only
pytest tests/unit -v

# Integration tests only
pytest tests/integration -v

# E2E tests only
pytest tests/e2e -v
```

### Run with Coverage
```bash
pytest --cov=app --cov-report=html
# Open htmlcov/index.html to view coverage report
```

### Install Playwright (for E2E tests)
```bash
playwright install --with-deps chromium
```

## 📊 Test Coverage

The project maintains high test coverage across all layers:

- **Unit Tests**: Test individual functions and business logic
  - Calculator operations
  - Analytics calculations
  - Security functions
  
- **Integration Tests**: Test API endpoints with database
  - Authentication flows
  - BREAD operations
  - Analytics endpoints
  - User profile management

- **E2E Tests**: Test complete user workflows with Playwright
  - Registration and login
  - Performing calculations
  - Viewing history and analytics
  - Profile updates
  - Navigation flows

**Target Coverage**: >90%

## 🚢 Deployment

### Docker Hub
The application is automatically deployed to Docker Hub via GitHub Actions.
```bash
# Pull the latest image
docker pull jaiagosto/calculator-app:latest

# Run the container
docker run -p 8000:8000 \
  -e DATABASE_URL=your_db_url \
  -e REDIS_URL=your_redis_url \
  -e SECRET_KEY=your_secret_key \
  jaiagosto/calculator-app:latest
```

### CI/CD Pipeline
The GitHub Actions workflow automatically:
1. Runs all tests (unit, integration, E2E)
2. Performs security scanning with Trivy
3. Builds Docker image
4. Pushes to Docker Hub (on main branch)

## 🔐 Security Best Practices

- ✅ Password hashing with bcrypt
- ✅ JWT token authentication
- ✅ Token blacklisting for logout
- ✅ Environment variable configuration
- ✅ SQL injection prevention via ORM
- ✅ Input validation with Pydantic
- ✅ CORS configuration
- ✅ Security scanning in CI/CD

## 📝 API Documentation

### Authentication Endpoints
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get token
- `POST /auth/logout` - Logout (blacklist token)
- `GET /auth/me` - Get current user info

### Calculation Endpoints (BREAD)
- `GET /calculations/` - Browse all calculations
- `POST /calculations/` - Add new calculation
- `GET /calculations/{id}` - Read specific calculation
- `PUT /calculations/{id}` - Edit calculation
- `DELETE /calculations/{id}` - Delete calculation

### Analytics Endpoints
- `GET /analytics/summary` - Get analytics summary
- `GET /analytics/history` - Get calculation history (with filters)
- `DELETE /analytics/history` - Clear all history

### User Profile Endpoints
- `GET /users/profile` - Get user profile
- `PUT /users/profile` - Update profile
- `POST /users/change-password` - Change password
- `DELETE /users/profile` - Delete account

Full interactive API documentation available at `/api/docs` when running.

## 🎓 Learning Outcomes Demonstrated

### CLO3: Python Applications with Automated Testing
- Comprehensive test suite with pytest
- Unit, integration, and E2E tests
- >90% code coverage

### CLO4: GitHub Actions CI/CD
- Automated testing on push/PR
- Docker image building and pushing
- Security scanning integration

### CLO9: Containerization with Docker
- Multi-container setup with docker-compose
- Optimized Dockerfile
- Environment configuration

### CLO10: REST API Creation & Testing
- FastAPI REST endpoints
- Comprehensive API testing
- OpenAPI documentation

### CLO11: SQL Database Integration
- PostgreSQL with SQLAlchemy ORM
- Proper database migrations
- Data relationships

### CLO12: JSON Serialization with Pydantic
- Request/response validation
- Type safety
- Automatic documentation

### CLO13: Security Best Practices
- JWT authentication
- Password hashing
- Token blacklisting
- Input validation

## 👨‍💻 Author

**Jailene Agosto**
- GitHub: [@jaiagosto](https://github.com/jaiagosto)
- Docker Hub: [@jaiagosto](https://hub.docker.com/u/jaiagosto)
- Institution: New Jersey Institute of Technology (NJIT)
- Course: IS601855 - Python for Web API Development

## 📄 License

This project is submitted as coursework for IS601855 at NJIT.

## 🙏 Acknowledgments

- Professor Keith Williams - IS601 Web Systems Development
- FastAPI documentation and community
- SQLAlchemy documentation
- Playwright testing framework

---

**Note**: This application was developed as a final project demonstrating proficiency in full-stack web development, including backend APIs, frontend development, database integration, authentication, testing, and DevOps practices.