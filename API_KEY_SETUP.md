# API Key Setup Instructions

This document explains how to configure API keys for the Investment Banking Research App.

## 📋 Required API Keys

### Perplexity AI API Key
- **Service**: Perplexity AI (for LLM research calls)
- **Required**: Yes
- **Get your key**: https://perplexity.ai/settings/api

## 🔧 Configuration Methods

### Method 1: Environment Variables (.env file) - RECOMMENDED
1. Open the `.env` file in the project root directory
2. Replace `your-perplexity-api-key-here` with your actual API key:
   ```
   PERPLEXITY_API_KEY=your-actual-api-key-here
   ```
3. Save the file

### Method 2: Direct Configuration (config.py) - FALLBACK
If the .env method doesn't work, you can set the API key directly in `config.py`:

1. Open `config.py` file
2. Find line 21 (around line 21):
   ```python
   # PERPLEXITY_API_KEY = "your-api-key-here"
   ```
3. Uncomment and replace with your actual API key:
   ```python
   PERPLEXITY_API_KEY = "your-actual-api-key-here"
   ```
4. Save the file

### Method 3: Streamlit Sidebar (Runtime)
The app also provides a sidebar input for entering your API key at runtime:
- When you run the app, look for the API key input in the left sidebar
- Enter your Perplexity API key there
- This method doesn't require editing any files

## 🔒 Security Best Practices

1. **Never commit API keys to version control**
   - The `.env` file is already in `.gitignore`
   - Always use placeholder values in committed code

2. **Environment Variables Priority**
   The app checks for API keys in this order:
   1. Streamlit sidebar input (highest priority)
   2. Environment variables from `.env` file
   3. Direct configuration in `config.py`
   4. System environment variables

3. **Production Deployment**
   - For production, set environment variables directly on your hosting platform
   - Don't rely on `.env` files in production environments

## 🚀 Quick Start

1. Copy `.env.example` to `.env` (if not already done):
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your API key:
   ```
   PERPLEXITY_API_KEY=your-actual-perplexity-api-key-here
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

## ✅ Verification

To verify your API key is working:
1. Run the app with `streamlit run app.py`
2. Check the console output for messages like:
   ```
   ✅ [CONFIG] Perplexity API key configured: XX characters
   ```
3. Try generating a presentation - if it works, your API key is configured correctly

## 🔍 Troubleshooting

### "No API key found" error
- Check that your `.env` file exists and has the correct format
- Ensure there are no extra spaces around the equals sign
- Try Method 2 (direct config.py configuration) as a fallback

### API calls failing
- Verify your API key is valid at https://perplexity.ai/settings/api
- Check your API usage limits and billing status
- Ensure your internet connection is working

### File not found errors
- Make sure you're in the correct project directory
- Verify all required files are present (see README.md for full setup)

## 📞 Support

If you continue having issues:
1. Check the console output for detailed error messages
2. Verify your API key works with a simple test call
3. Ensure all dependencies are installed: `pip install -r requirements.txt`

---
*This app was created for investment banking research and presentation generation using AI.*