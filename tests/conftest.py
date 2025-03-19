import pytest
from text2sql.app.agents import TextTranslatorAgent, SQLGeneratorAgent, TextToSQLPipeline

@pytest.fixture
def text_translator():
    return TextTranslatorAgent()

@pytest.fixture
def sql_generator():
    return SQLGeneratorAgent()

@pytest.fixture
def pipeline():
    return TextToSQLPipeline() 