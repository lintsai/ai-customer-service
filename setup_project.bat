@echo off
setlocal enabledelayedexpansion

echo Starting project setup in %CD%...

:: Create docker directory
mkdir docker 2>nul
type nul > docker\Dockerfile
type nul > docker\docker-compose.yml

:: Create docs directory
mkdir docs\api docs\architecture docs\deployment 2>nul
type nul > docs\api\README.md
type nul > docs\architecture\README.md
type nul > docs\deployment\README.md

:: Create source code directory structure
mkdir src\api\routes src\api\middlewares src\api\validators 2>nul
type nul > src\api\__init__.py
type nul > src\api\routes\__init__.py
type nul > src\api\middlewares\__init__.py
type nul > src\api\validators\__init__.py

mkdir src\core 2>nul
type nul > src\core\__init__.py
type nul > src\core\config.py
type nul > src\core\security.py
type nul > src\core\logging.py

mkdir src\llm\prompts src\llm\models 2>nul
type nul > src\llm\__init__.py
type nul > src\llm\engine.py
type nul > src\llm\prompts\__init__.py
type nul > src\llm\models\__init__.py

mkdir src\rag 2>nul
type nul > src\rag\__init__.py
type nul > src\rag\retriever.py
type nul > src\rag\indexer.py
type nul > src\rag\vectorstore.py

mkdir src\memory 2>nul
type nul > src\memory\__init__.py
type nul > src\memory\buffer.py
type nul > src\memory\summary.py

mkdir src\db\mongodb src\db\redis src\db\postgres 2>nul
type nul > src\db\__init__.py
type nul > src\db\mongodb\__init__.py
type nul > src\db\redis\__init__.py
type nul > src\db\postgres\__init__.py

mkdir src\services 2>nul
type nul > src\services\__init__.py
type nul > src\services\chat.py
type nul > src\services\knowledge.py
type nul > src\services\user.py

mkdir src\utils 2>nul
type nul > src\utils\__init__.py
type nul > src\utils\helpers.py

:: Create test directory
mkdir tests\unit tests\integration tests\e2e 2>nul
type nul > tests\unit\__init__.py
type nul > tests\integration\__init__.py
type nul > tests\e2e\__init__.py

:: Create root directory files
type nul > .env
type nul > .gitignore
type nul > README.md
type nul > requirements.txt
type nul > main.py

:: Create .gitignore content
echo # Python > .gitignore
echo __pycache__/ >> .gitignore
echo *.py[cod] >> .gitignore
echo *$py.class >> .gitignore
echo *.so >> .gitignore
echo .Python >> .gitignore
echo build/ >> .gitignore
echo develop-eggs/ >> .gitignore
echo dist/ >> .gitignore
echo downloads/ >> .gitignore
echo eggs/ >> .gitignore
echo .eggs/ >> .gitignore
echo lib/ >> .gitignore
echo lib64/ >> .gitignore
echo parts/ >> .gitignore
echo sdist/ >> .gitignore
echo var/ >> .gitignore
echo wheels/ >> .gitignore
echo *.egg-info/ >> .gitignore
echo .installed.cfg >> .gitignore
echo *.egg >> .gitignore
echo # Virtual Environment >> .gitignore
echo venv/ >> .gitignore
echo ENV/ >> .gitignore
echo # IDE >> .gitignore
echo .idea/ >> .gitignore
echo .vscode/ >> .gitignore
echo *.swp >> .gitignore
echo *.swo >> .gitignore
echo # Environment variables >> .gitignore
echo .env >> .gitignore
echo # Database >> .gitignore
echo *.db >> .gitignore
echo *.sqlite3 >> .gitignore

:: Create requirements.txt content
echo fastapi==0.104.1 > requirements.txt
echo uvicorn==0.24.0 >> requirements.txt
echo langchain==0.0.341 >> requirements.txt
echo python-dotenv==1.0.0 >> requirements.txt
echo pydantic==2.4.2 >> requirements.txt
echo pymongo==4.6.0 >> requirements.txt
echo redis==5.0.1 >> requirements.txt
echo sqlalchemy==2.0.23 >> requirements.txt
echo psycopg2-binary==2.9.9 >> requirements.txt
echo milvus-python-sdk==2.3.1 >> requirements.txt
echo python-jose==3.3.0 >> requirements.txt
echo passlib==1.7.4 >> requirements.txt
echo prometheus-client==0.18.0 >> requirements.txt
echo pytest==7.4.3 >> requirements.txt
echo requests==2.31.0 >> requirements.txt
echo sentence-transformers==2.2.2 >> requirements.txt
echo transformers==4.35.1 >> requirements.txt
echo torch==2.1.1 >> requirements.txt

:: Create .env file content
echo # API Settings > .env
echo API_HOST=0.0.0.0 >> .env
echo API_PORT=8000 >> .env
echo API_DEBUG=True >> .env
echo # Database Settings >> .env
echo MONGO_URI=mongodb://localhost:27017 >> .env
echo REDIS_URI=redis://localhost:6379 >> .env
echo POSTGRES_URI=postgresql://user:pass@localhost:5432/db >> .env
echo # LLM Settings >> .env
echo LLM_MODEL=gpt-3.5-turbo >> .env
echo LLM_TEMPERATURE=0.7 >> .env
echo LLM_MAX_TOKENS=800 >> .env
echo # Security Settings >> .env
echo JWT_SECRET_KEY=your-secret-key >> .env
echo JWT_ALGORITHM=HS256 >> .env

:: Create main.py content
echo from fastapi import FastAPI > main.py
echo from src.core.config import settings >> main.py
echo. >> main.py
echo app = FastAPI( >> main.py
echo     title="AI Customer Service System", >> main.py
echo     description="An AI-powered customer service system", >> main.py
echo     version="1.0.0" >> main.py
echo ) >> main.py
echo. >> main.py
echo @app.get("/") >> main.py
echo async def root(): >> main.py
echo     return {"message": "Welcome to AI Customer Service System"} >> main.py
echo. >> main.py
echo if __name__ == "__main__": >> main.py
echo     import uvicorn >> main.py
echo     uvicorn.run( >> main.py
echo         "main:app", >> main.py
echo         host=settings.API_HOST, >> main.py
echo         port=settings.API_PORT, >> main.py
echo         reload=settings.DEBUG >> main.py
echo     ) >> main.py

:: Ask about virtual environment setup
set /p answer=Do you want to create a virtual environment and install dependencies? (y/n)
if /i "%answer%"=="y" (
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
)

echo Project structure setup completed!
pause