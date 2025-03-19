from setuptools import setup, find_packages

setup(
    name="text2sql",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "pydantic>=1.8.0",
        "openai>=1.6.1",
        "python-dotenv>=0.19.0",
        "pytest>=7.0.0",
        "httpx>=0.24.0",
        "sqlparse==0.4.4",
        "python-jose==3.3.0"
    ],
) 