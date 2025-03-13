# SierraServer


## Getting Started
### Prerequisites
Ensure you have the following installed:
- Python 3.9+
- pip
- Bash (for running the start script)

### Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/HFZR2005/SierraServer.git
cd SierraServer
pip install -r requirements.txt
```

Download the `tools` folder for the classifier model files from:
(https://drive.google.com/drive/u/0/folders/1Fa53W6K1AQ1J_PDEHoF7VsPQZUoEUooa)
```bash
unzip tools.zip -d tools
mv tools/* ./tools 
```

Install PyTorch manually (depending on CPU or GPU):

If you have a GPU:
```bash
pip install torch
```

If you don't have a GPU:
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
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

Also make sure that your Mistral API key is available in the environment variable `MISTRAL_API_KEY` before running the server. Do this by opening the .env file and adding the key there. On UNIX systems, you can do this by running the following command:

```bash
echo "MISTRAL_API_KEY=your_api_key_here" > .env
```

## Project Structure
```
.
├── app.py                         # Main FastAPI application
├── .gitattributes
├── .gitignore
├── main.py                        # Entry point 
├── README.md
├── requirements.txt               # Project dependencies
├── start_uvicorn.sh               # Bash script to start the server in the background
├── tests
│   ├── __init__py
│   └── test_similarity.py
└── tools                          # Modular tool files FROM GDRIVE LINK
```

## Contributing
### Adding a New Feature
1. **Create a new branch**:
   - Create a new branch with a descriptive name e.g. feature/toolname
   - Make your changes in this branch.

2. **Create a New Tool**:
   - Add a new Python file inside the `tools/` directory.
   - Implement the required functionality.

3. **Register the Tool in `app.py`**:
   - Import the tool inside `app.py`.
   - Add an appropriate FastAPI endpoint.

4. **Test Your Changes**:
   - Ensure the application runs without errors.
   - Write tests if applicable.

5. **Create a Pull Request**:
    - Push your changes to the remote repository.
    - Create a pull request on GitHub.



