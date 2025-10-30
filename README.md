# Swarmchestrate GUI
A GUI for registering capacities and applications in Swarmchestrate.

## Prerequisites
The following prerequisites should be installed before getting started:
- **Git**: for cloning the repository
- **Python**: version 3.10 or later
- **pip**: Python package manager
- **[Dart Sass](https://sass-lang.com/install/)**: to allow styles to work in the browser.
- **[Node.js](https://nodejs.org/en/download)**: for Bootstrap Sass files.

## Getting Started
### 1. Clone the repository
```bash
git clone git@github.com:Swarmchestrate/gui.git
```
### 2. Navigate to the project directory
```bash
cd gui
```
### 3. Make and activate the Python virtual environment
```bash
python3 -m venv venv
source venv/bin/activate # or source venv.sh
```
### 4. Install packages in requirements.txt
```bash
pip install -r requirements.txt
```
### 5. Install dependencies in package.json
```bash
npm install
```
### 6. Set up the .env file
Rename or copy the example file to `.env`
```bash
cp .env_example .env
```
> [!NOTE]
> The following environment variables have to be set manually:
> - `SECRET_KEY`: see the [Django documentation](https://docs.djangoproject.com/en/5.2/ref/settings/#secret-key) for guidance on how to set this (for development purposes, this can be any value).
> - `API_URL`: the URL for the API used to generate parts of the GUI (not publicly shareable).
## Running the GUI
To run the GUI locally in your browser, ensure the virtual environment is activated beforehand, then use the `run.sh` script to run the GUI:
```bash
source venv.sh
python3 manage.py runserver # or ./run.sh
```
