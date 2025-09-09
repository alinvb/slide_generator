#!/bin/bash

# Create a fake machine-id file with safe content
export FAKE_MACHINE_ID="/tmp/safe_machine_id"
echo "streamlit-safe-machine-id-$(date +%s)" > "$FAKE_MACHINE_ID"

# Set environment variables to disable all metrics
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
export STREAMLIT_GLOBAL_DEVELOPMENT_MODE=false
export STREAMLIT_SERVER_HEADLESS=true
export PYTHONIOENCODING=utf-8
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

# Try to replace system machine-id files temporarily (if we have permission)
if [ -w /etc/machine-id ] 2>/dev/null; then
    echo "backup-$(cat /etc/machine-id)" > /etc/machine-id.bak 2>/dev/null
    cp "$FAKE_MACHINE_ID" /etc/machine-id 2>/dev/null
fi

# Start Streamlit
cd /home/user/webapp
streamlit run app.py --server.port=8502 --server.address=0.0.0.0 --server.headless=true --server.fileWatcherType=none --server.enableXsrfProtection=false --global.developmentMode=false --browser.gatherUsageStats=false