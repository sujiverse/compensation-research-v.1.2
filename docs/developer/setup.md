# 🛠️ Development Setup Guide

> **Complete guide to setting up a local development environment**

## 🎯 Prerequisites

### **System Requirements**
```yaml
Operating System:
  - Windows 10/11, macOS 10.15+, or Linux (Ubuntu 18.04+)

Python:
  - Version: 3.11 or higher
  - Virtual environment: venv or conda

Memory: 8GB RAM minimum (16GB recommended)
Storage: 20GB free space
Network: Stable internet for API access
```

### **Required Tools**
```bash
# Essential development tools
git                    # Version control
python3.11+           # Python interpreter
pip                   # Package manager
docker                # Containerization (optional)
```

### **Optional Tools**
```bash
# Recommended development tools
vscode                # IDE with Python extensions
postman              # API testing
obsidian             # Vault visualization
github-cli           # GitHub integration
```

## 🚀 Quick Development Setup

### **1. Repository Setup**
```bash
# Clone the repository
git clone https://github.com/your-username/compensation-research.git
cd compensation-research

# Create and activate virtual environment
python -m venv compensation_dev_env

# Activate environment
# On Windows:
compensation_dev_env\Scripts\activate
# On macOS/Linux:
source compensation_dev_env/bin/activate

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### **2. Environment Configuration**
```bash
# Copy environment template
cp .env.example .env.development

# Edit development configuration
nano .env.development
```

**Development Environment Variables**:
```bash
# Core Settings
ENVIRONMENT=development
LOG_LEVEL=DEBUG
DEBUG=true

# Development Database
POSTGRES_URL=sqlite:///dev_compensation.db
REDIS_URL=

# API Settings
RESEARCH_CYCLE_INTERVAL=3600  # 1 hour for development
MAX_PAPERS_PER_CYCLE=2        # Limit for testing

# Development Features
DEV_MODE=true
DEV_MOCK_API=false
DEV_SAMPLE_DATA=true

# Testing
TEST_DATABASE_URL=sqlite:///test_compensation.db
TEST_VAULT_PATH=test-vault-dev
```

### **3. Development Database Setup**
```bash
# Initialize development database
python scripts/init_dev_db.py

# Run database migrations (if applicable)
python scripts/migrate_db.py

# Seed with development data
python scripts/seed_dev_data.py
```

### **4. Verify Installation**
```bash
# Run system health check
python scripts/health_check.py

# Run integration tests
python test_integration.py

# Test individual components
python paper_screener.py --test
python why_analyzer.py --test
python node_connector.py --test
python obsidian_generator.py --test
```

## 🔧 IDE Configuration

### **Visual Studio Code Setup**

#### **Required Extensions**
```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.pylint",
    "ms-python.black-formatter",
    "ms-python.isort",
    "ms-python.mypy-type-checker",
    "ms-toolsai.jupyter",
    "github.copilot",
    "redhat.vscode-yaml",
    "yzhang.markdown-all-in-one"
  ]
}
```

#### **Workspace Settings**
```json
{
  "python.defaultInterpreterPath": "./compensation_dev_env/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length", "88"],
  "python.sortImports.args": ["--profile", "black"],
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests/"],
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    ".coverage": true,
    "htmlcov/": true
  }
}
```

#### **Launch Configuration**
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Run Single Analysis",
      "type": "python",
      "request": "launch",
      "program": "compensation_research_system.py",
      "args": ["--single", "--debug"],
      "console": "integratedTerminal",
      "envFile": ".env.development"
    },
    {
      "name": "Test Paper Screener",
      "type": "python",
      "request": "launch",
      "program": "paper_screener.py",
      "args": ["--test"],
      "console": "integratedTerminal"
    },
    {
      "name": "Run Tests",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": ["tests/", "-v"],
      "console": "integratedTerminal"
    }
  ]
}
```

### **PyCharm Setup**

#### **Project Configuration**
1. Open project in PyCharm
2. Configure Python interpreter: Settings → Project → Python Interpreter
3. Select the virtual environment: `./compensation_dev_env/bin/python`
4. Configure code style: Settings → Editor → Code Style → Python
5. Set line length to 88 (Black formatter standard)

#### **Run Configurations**
```yaml
Single Analysis:
  - Script path: compensation_research_system.py
  - Parameters: --single --debug
  - Environment variables: Load from .env.development

Component Tests:
  - Script path: pytest
  - Parameters: tests/ -v
  - Working directory: project root
```

## 🧪 Testing Setup

### **Test Environment Configuration**
```bash
# Create test-specific environment file
cp .env.example .env.test

# Configure test settings
echo "ENVIRONMENT=test
LOG_LEVEL=DEBUG
TEST_MODE=true
USE_MOCK_DATA=true
TEST_DATABASE_URL=sqlite:///test.db
TEST_VAULT_PATH=test-vault" > .env.test
```

### **Running Tests**
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test categories
pytest tests/unit/          # Unit tests only
pytest tests/integration/   # Integration tests only
pytest tests/performance/   # Performance tests only

# Run tests with detailed output
pytest -v -s

# Run tests in parallel
pytest -n auto
```

### **Test Data Setup**
```bash
# Generate test data
python scripts/generate_test_data.py

# Create mock API responses
python scripts/create_mock_responses.py

# Setup test fixtures
python scripts/setup_test_fixtures.py
```

## 🔍 Debugging Configuration

### **Logging Setup**
```python
# Development logging configuration
import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dev_debug.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Component-specific loggers
paper_logger = logging.getLogger('paper_screener')
why_logger = logging.getLogger('why_analyzer')
node_logger = logging.getLogger('node_connector')
obsidian_logger = logging.getLogger('obsidian_generator')
```

### **Debug Utilities**
```python
# Debug helper functions
def debug_paper_analysis(paper_id: str):
    """Debug a specific paper analysis"""
    logger = logging.getLogger('debug')

    logger.debug(f"Starting analysis for paper: {paper_id}")

    # Enable detailed tracing
    screener = CompensationPaperScreener(debug=True)
    analyzer = CompensationWhyAnalyzer(debug=True)

    # Step-by-step analysis
    paper_data = screener.get_paper_by_id(paper_id)
    logger.debug(f"Paper data: {paper_data}")

    analysis = analyzer.analyze_paper(paper_data)
    logger.debug(f"Analysis result: {analysis}")

    return analysis

def debug_connection_strength(node1_id: str, node2_id: str):
    """Debug connection strength calculation"""
    connector = CompensationNodeConnector(debug=True)

    node1 = connector.get_node(node1_id)
    node2 = connector.get_node(node2_id)

    strength = connector.calculate_connection_strength(node1, node2)

    print(f"Connection strength between {node1.title} and {node2.title}: {strength}")
    print(f"Detailed breakdown: {connector.get_strength_breakdown()}")
```

### **Performance Profiling**
```bash
# Profile specific functions
python -m cProfile -o profile_results.prof paper_screener.py

# Memory profiling
python -m memory_profiler compensation_research_system.py

# Line-by-line profiling
kernprof -l -v why_analyzer.py
```

## 🛠️ Development Workflow

### **Branch Strategy**
```bash
# Feature development
git checkout -b feature/improved-pattern-recognition
# Make changes...
git commit -m "feat: improve pattern recognition accuracy"
git push origin feature/improved-pattern-recognition
# Create pull request

# Bug fixes
git checkout -b bugfix/fix-connection-scoring
# Make changes...
git commit -m "fix: correct connection strength calculation"

# Hot fixes
git checkout -b hotfix/urgent-api-fix
# Make changes...
git commit -m "hotfix: resolve API timeout issue"
```

### **Code Quality Checks**
```bash
# Pre-commit setup
pip install pre-commit
pre-commit install

# Manual quality checks
black .                    # Format code
isort .                   # Sort imports
flake8 .                  # Lint code
mypy .                    # Type checking
bandit -r .               # Security scanning
```

### **Development Commands**
```bash
# Start development server (if applicable)
python -m compensation_research_system --dev-server

# Watch for file changes and auto-restart
watchmedo auto-restart --directory=. --pattern=*.py --recursive -- python compensation_research_system.py --single

# Generate development documentation
sphinx-build -b html docs/ docs/_build/

# Create development database backup
python scripts/backup_dev_db.py
```

## 🔧 Advanced Development Setup

### **Docker Development Environment**
```dockerfile
# Dockerfile.dev
FROM python:3.11-slim

WORKDIR /app

# Install development dependencies
COPY requirements.txt requirements-dev.txt ./
RUN pip install -r requirements.txt -r requirements-dev.txt

# Copy source code
COPY . .

# Development command
CMD ["python", "compensation_research_system.py", "--dev-mode"]
```

```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  compensation-research-dev:
    build:
      context: .
      dockerfile: Dockerfile.dev
    volumes:
      - .:/app
      - dev-vault:/app/Compensation-Research-Vault
    environment:
      - ENVIRONMENT=development
      - LOG_LEVEL=DEBUG
    ports:
      - "8080:8080"
    depends_on:
      - redis-dev
      - postgres-dev

  redis-dev:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  postgres-dev:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: compensation_dev
      POSTGRES_USER: dev_user
      POSTGRES_PASSWORD: dev_password
    ports:
      - "5432:5432"
    volumes:
      - postgres-dev-data:/var/lib/postgresql/data

volumes:
  dev-vault:
  postgres-dev-data:
```

### **API Development Server**
```python
# dev_server.py
from flask import Flask, jsonify, request
from compensation_research_system import CompensationResearchSystem

app = Flask(__name__)
system = CompensationResearchSystem()

@app.route('/api/v1/analyze', methods=['POST'])
def analyze_paper():
    paper_data = request.json
    analysis = system.analyze_paper(paper_data)
    return jsonify(analysis.__dict__)

@app.route('/api/v1/status', methods=['GET'])
def get_status():
    status = system.get_status()
    return jsonify(status)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
```

### **Development Monitoring**
```python
# dev_monitor.py
import time
import psutil
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class DevelopmentMonitor(FileSystemEventHandler):
    def __init__(self):
        self.logger = logging.getLogger('dev_monitor')

    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            self.logger.info(f"File modified: {event.src_path}")
            self.run_tests()

    def run_tests(self):
        """Run relevant tests when files change"""
        # Implement smart test running based on changed files
        pass

    def monitor_performance(self):
        """Monitor system performance during development"""
        process = psutil.Process()
        self.logger.info(f"Memory usage: {process.memory_info().rss / 1024 / 1024:.2f} MB")
        self.logger.info(f"CPU usage: {process.cpu_percent():.2f}%")

# Start monitoring
if __name__ == '__main__':
    monitor = DevelopmentMonitor()
    observer = Observer()
    observer.schedule(monitor, path='.', recursive=True)
    observer.start()

    try:
        while True:
            monitor.monitor_performance()
            time.sleep(60)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
```

## 📚 Development Resources

### **Documentation Generation**
```bash
# Generate API documentation
sphinx-apidoc -o docs/api/ .

# Build documentation
sphinx-build -b html docs/ docs/_build/

# Serve documentation locally
python -m http.server 8000 --directory docs/_build/
```

### **Database Management**
```python
# Database migration scripts
def create_dev_tables():
    """Create development database tables"""
    # Implementation here
    pass

def seed_dev_data():
    """Seed database with development data"""
    # Implementation here
    pass

def reset_dev_database():
    """Reset development database to clean state"""
    # Implementation here
    pass
```

### **Performance Testing**
```python
# Performance test utilities
import time
import functools

def performance_test(func):
    """Decorator to measure function performance"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        print(f"{func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    return wrapper

@performance_test
def test_paper_screening_performance():
    """Test paper screening performance with large dataset"""
    screener = CompensationPaperScreener()
    papers = screener.screen_papers(limit=100)
    return len(papers)
```

---

**🛠️ This development setup provides a comprehensive environment for contributing to the Compensation Research System with proper tooling, testing, and debugging capabilities.**