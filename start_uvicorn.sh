pkill uvicorn

# Run Uvicorn in the background with nohup
nohup uvicorn app:app --host 0.0.0.0 --port 8000 > uvicorn.log 2>&1 &

# Get the PID of the Uvicorn process and save it
if pgrep uvicorn > /dev/null; then
    echo "Uvicorn started successfully! Check logs using: tail -f uvicorn.log"
fi