# SierraServer


# Project Contribution Guide


## Getting Started
### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- pip
- Bash (for running the start script)

### Installation
Clone the repository and install dependencies:
```bash
git clone git@github.com:HFZR2005/SierraServer.git
cd SierraServer
pip install -r requirements.txt
```

### Running the Application
Before starting the server, ensure the `start_uvicorn.sh` script is executable:
```bash
chmod +x start_uvicorn.sh
./start_uvicorn.sh
```
This will launch the FastAPI server in the background.

To make the server run in the foreground, just run the main.py file using: 

```bash
python main.py
```

## Project Structure
```
.
├── README.md
├── app.py                 # Main FastAPI application
├── main.py                # Entry point 
├── requirements.txt       # Project dependencies
├── start_uvicorn.sh       # Bash script to start the server in the background
└── tools                  # Modular tool files
    ├── __init__.py        # Makes tools a package
    ├── categorize_question.py
    ├── conversational_child.py
    └── scenario.py
```

## Contributing
### Adding a New Feature
1. **Create a New Tool**:
   - Add a new Python file inside the `tools/` directory.
   - Implement the required functionality.

2. **Register the Tool in `app.py`**:
   - Import the tool inside `app.py`.
   - Add an appropriate FastAPI endpoint.

3. **Test Your Changes**:
   - Ensure the application runs without errors.
   - Write tests if applicable.



Thank you for contributing!
