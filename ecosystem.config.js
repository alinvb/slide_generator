module.exports = {
  apps: [{
    name: 'investment-banking-app',
    script: 'streamlit',
    args: 'run app.py --server.port 8504 --server.address 0.0.0.0',
    cwd: '/home/user/webapp',
    env: {
      NODE_ENV: 'production'
    },
    error_file: './logs/streamlit-error.log',
    out_file: './logs/streamlit-out.log',
    log_file: './logs/streamlit.log',
    time: true,
    autorestart: true,
    max_restarts: 10,
    min_uptime: '10s'
  }]
};