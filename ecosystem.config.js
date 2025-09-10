module.exports = {
  apps: [{
    name: 'investment-banking-app',
    script: 'python',
    args: '-m streamlit run app.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true --server.fileWatcherType=none',
    cwd: '/home/user/webapp',
    env: {
      'PYTHONPATH': '/home/user/webapp',
      'STREAMLIT_SERVER_PORT': '8501',
      'STREAMLIT_SERVER_ADDRESS': '0.0.0.0'
    },
    max_memory_restart: '1G',
    log_date_format: 'YYYY-MM-DD HH:mm:ss',
    merge_logs: true,
    out_file: './logs/streamlit-out.log',
    error_file: './logs/streamlit-error.log'
  }]
};