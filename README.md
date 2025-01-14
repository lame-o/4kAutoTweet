# 🖼️ 4K Tweet Bot

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Twitter bot that posts 4K images with contextual captions. Using AI to analyze images and generate engaging captions, it promotes the new "click and hold" feature for viewing high-resolution content.

<p align="center">
  <img src="https://img.shields.io/badge/Powered%20by-Hugging%20Face%20🤗-orange" alt="Powered by Hugging Face">
  <img src="https://img.shields.io/badge/AI-GPT--4-green" alt="GPT-4">
</p>

## ✨ Features

- 🤖 **Smart Captions**: Uses AI to understand image content and generate relevant captions
- 🔄 **Regular Updates**: Posts every 3 hours to maintain consistent engagement
- 🎯 **Feature Focus**: Promotes Twitter's "click and hold" 4K viewing experience
- 🔒 **Secure**: Environment variables for all sensitive credentials
- 🎨 **Adaptable**: Works with any collection of high-quality images

## 🛠️ Tech Stack

- **Core**: Python 3.12
- **AI Models**:
  - Hugging Face Transformers for BLIP image analysis
  - OpenAI GPT-4 for natural language caption generation
- **APIs**: Twitter API v2 via Tweepy
- **Scheduling**: Python Schedule library

## 📦 Dependencies

```bash
tweepy==4.14.0          # Twitter API interactions
requests==2.31.0        # HTTP requests
schedule==1.2.1         # Task scheduling
python-dotenv==1.0.0    # Environment management
Pillow==10.1.0         # Image processing
torch==2.2.0           # ML framework
transformers==4.36.2    # Hugging Face Transformers
openai==0.28.0         # OpenAI API
```

## 🚀 Quick Start

1. **Clone & Install**
   ```bash
   git clone https://github.com/yourusername/4k-tweet-bot.git
   cd 4k-tweet-bot
   pip install -r requirements.txt
   ```

2. **Configure**
   - Copy `.env.example` to `.env`
   - Add your API credentials:
     ```env
     X_API_KEY=your_key
     X_API_SECRET_KEY=your_secret
     X_ACCESS_TOKEN=your_token
     X_ACCESS_TOKEN_SECRET=your_token_secret
     Client_ID=your_client_id
     Client_Secret=your_client_secret
     OPENAI_API_KEY=your_openai_key
     ```

3. **Add Images**
   - Place your 4K images in the `images/` directory
   - Supported formats: `.jpg`, `.jpeg`, `.png`

4. **Run**
   ```bash
   python bot.py
   ```

## 🎯 Caption Style

The bot crafts concise, engaging captions that:
- Stay under 25 characters
- Reference image content
- Promote the 4K viewing feature
- Use minimal emojis
- Sound natural and trendy

## 🔜 Future Enhancements

- Integration with Unsplash API for dynamic image sourcing
- Enhanced image analysis capabilities
- Custom caption templates
- Engagement analytics

## 📝 License

This project is MIT licensed. See [LICENSE](LICENSE) for details.

---
<p align="center">
Made with 💻 and ☕
</p>