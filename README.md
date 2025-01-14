# 4K Tweet Bot

A Twitter bot that posts stunning 4K images with contextual captions.

## Features

- Posts random 4K images from a local directory every 3 hours
- Uses AI-powered image analysis to understand image content
- Generates unique, engaging captions that reference the image content
- Promotes the "click and hold" feature for viewing images in 4K
- Secure API key management through environment variables

## Tech Stack

- Python 3.12
- Tweepy for Twitter API interaction
- Hugging Face Transformers for BLIP image analysis
- OpenAI GPT-4 for natural language caption generation
- Schedule for automated posting

## Dependencies

```
tweepy==4.14.0
requests==2.31.0
schedule==1.2.1
python-dotenv==1.0.0
Pillow==10.1.0
torch==2.2.0
transformers==4.36.2  # Hugging Face Transformers library
openai==0.28.0
```

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your API keys:
```
X_API_KEY=your_api_key
X_API_SECRET_KEY=your_api_secret
X_ACCESS_TOKEN=your_access_token
X_ACCESS_TOKEN_SECRET=your_access_token_secret
Client_ID=your_client_id
Client_Secret=your_client_secret
OPENAI_API_KEY=your_openai_api_key
```
4. Add your 4K images to the `images` directory
5. Run the bot: `python bot.py`

## How It Works

1. Every 3 hours, the bot:
   - Selects a random 4K image from the `images` directory
   - Uses BLIP to analyze and understand the image content
   - Generates a unique caption using GPT-4 that:
     - References what's in the image
     - Promotes the "click and hold" feature
     - Maintains a casual, trendy tone
   - Posts the image and caption to Twitter

## Caption Style

The bot generates natural, engaging captions that:
- Keep it under 50 characters
- Reference the specific content of each image
- Mention the click/hold to load 4K feature
- Use at most one emoji
- Sound conversational and trendy
- Avoid generic templates

## Future Enhancements

Pulling images from unsplash.com but waiting on API access