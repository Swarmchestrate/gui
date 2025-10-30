# Swarmchestrate GUI
A GUI for registering capacities and applications in Swarmchestrate.

## Prerequisites
The following prerequisites should be installed before getting started:
- **Git**: for cloning the repository
- **Python**: version 3.10 or later
- **pip**: Python package manager
- **[Dart Sass](https://sass-lang.com/install/)**: to allow styles to work in the browser.
- **[Node.js](https://nodejs.org/en/download)**: for Bootstrap SASS files.

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
source venv.sh # venv/bin/activate
```
### 4. Install packages from requirements.txt
```bash
pip install -r requirements.txt
```
### 5. Set up the .env file
Rename or copy the example file to `.env`
```bash
cp .env_example .env
```
> [!NOTE]
> The `SECRET_KEY`, `OPENAPI_SPEC_URL` and `API_URL` variables are not set (the values for the `OPENAPI_SPEC_URL` and `API_URL` variables are not publicly shareable).
## Running the GUI
To run the GUI locally in your browser, ensure the virtual environment is activated beforehand, then use the `run.sh` script to run the GUI:
```bash
source venv.sh
./run.sh # python3 manage.py runserver
```
