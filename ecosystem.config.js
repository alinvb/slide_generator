module.exports = {
  apps: [{
    name: 'investment-banking-app',
    script: '/usr/local/bin/streamlit',
    args: 'run start_app.py --server.port=8502 --server.address=0.0.0.0 --server.headless=true --server.fileWatcherType=none --server.enableXsrfProtection=false --global.developmentMode=false --browser.gatherUsageStats=false --server.enableStaticServing=false',
    interpreter: 'none',
    cwd: '/home/user/webapp',
    env: {
      'PYTHONPATH': '/home/user/webapp',
      'STREAMLIT_SERVER_PORT': '8502',
      'STREAMLIT_SERVER_ADDRESS': '0.0.0.0',
      'PYTHONIOENCODING': 'utf-8',
      'LC_ALL': 'C.UTF-8',
      'LANG': 'C.UTF-8',
      'STREAMLIT_BROWSER_GATHER_USAGE_STATS': 'false',
      'STREAMLIT_GLOBAL_DEVELOPMENT_MODE': 'false',
      'STREAMLIT_SERVER_ENABLE_CORS': 'false',
      'STREAMLIT_SERVER_ENABLE_WEBSOCKET_COMPRESSION': 'false'
    },
    max_memory_restart: '1G',
    log_date_format: 'YYYY-MM-DD HH:mm:ss',
    merge_logs: true,
    out_file: './logs/streamlit-out.log',
    error_file: './logs/streamlit-error.log'
  }]
};