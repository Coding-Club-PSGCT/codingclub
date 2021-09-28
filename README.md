# Ideation site

The website created for Ideation hackathon held by Coding Club PSGCT.

## Getting started
- Install Python 3.9+
- Install Poetry  

Linux:
```zsh
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
```
Windows:
```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py -UseBasicParsing).Content | python -
```
- Install dependencies
```bash
# Install python dependencies
git clone "https://github.com/Coding-Club-PSGCT/codingclub.git"
cd codingclub
poetry install

# Install frontend dependencies
cd app/static
npm install
```

- Create instance specific config
```bash
# Create config file
cd ../../instance
touch config.py

# Set config values
echo "UPLOADS_DIR='full path to uploads directory'" >> config.py
echo "MAIL_PASSWORD='password to the mail account'" >> config.py
```
- Run server
```bash
cd ..
poetry run flask run
```

## Contributers
- [Jaswant Gunaseelan](https://github.com/Jaswant-G) 
- [Harshaa Vardaan](https://github.com/jaeger-2601)
