@echo off
echo Setting up VerbAndConjProj...
echo.

echo Creating virtual environment...
python -m venv .venv
echo.

echo Activating virtual environment...
call .venv\Scripts\activate
echo.

echo Installing dependencies...
pip install -r requirements.txt
echo.

echo Downloading SpaCy Italian model...
python -c "import spacy; spacy.cli.download('it_core_news_md')"
echo.

echo Setup complete! Run 'python main.py' to start.
echo.
pause