import os
import tweepy
import random
import schedule
import time
from datetime import datetime
from PIL import Image
from dotenv import load_dotenv
from transformers import pipeline
import openai

# Load environment variables
load_dotenv()

# X (Twitter) API credentials
CLIENT_ID = os.getenv('Client_ID')
CLIENT_SECRET = os.getenv('Client_Secret')
X_API_KEY = os.getenv('X_API_KEY')
X_API_SECRET_KEY = os.getenv('X_API_SECRET_KEY')
X_ACCESS_TOKEN = os.getenv('X_ACCESS_TOKEN')
X_ACCESS_TOKEN_SECRET = os.getenv('X_ACCESS_TOKEN_SECRET')

# OpenAI API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Constants
IMAGES_DIR = "images"
SUPPORTED_FORMATS = ('.jpg', '.jpeg', '.png')

# Initialize the models
print("Initializing models...")
image_captioner = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")
openai.api_key = OPENAI_API_KEY

def setup_x_api():
    """Initialize and return X API client"""
    try:
        # Verify credentials are not None
        if not all([CLIENT_ID, CLIENT_SECRET, X_API_KEY, X_API_SECRET_KEY, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET]):
            raise ValueError("Missing API credentials. Please check your .env file.")

        print(f"[{datetime.now()}] Initializing Twitter API client...")
        
        # Initialize OAuth 2.0 client
        oauth2_client = tweepy.Client(
            consumer_key=X_API_KEY,
            consumer_secret=X_API_SECRET_KEY,
            access_token=X_ACCESS_TOKEN,
            access_token_secret=X_ACCESS_TOKEN_SECRET,
            wait_on_rate_limit=True
        )
        
        # We still need v1.1 API for media upload
        auth = tweepy.OAuth1UserHandler(
            X_API_KEY, X_API_SECRET_KEY,
            X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET
        )
        api = tweepy.API(auth)
        
        # Test authentication
        try:
            me = oauth2_client.get_me()
            print(f"[{datetime.now()}] Authentication successful! Logged in as: @{me.data.username}")
        except Exception as e:
            print(f"[{datetime.now()}] Authentication failed: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response Status: {e.response.status_code}")
                print(f"Response Text: {e.response.text}")
            raise
        
        return oauth2_client, api
    except Exception as e:
        print(f"[{datetime.now()}] Error setting up API: {str(e)}")
        if isinstance(e, tweepy.TweepyException):
            print(f"Response Status: {getattr(e.response, 'status_code', 'N/A')}")
            print(f"Response Text: {getattr(e.response, 'text', 'N/A')}")
        raise

def get_random_image():
    """Get a random image from the images directory"""
    images = [f for f in os.listdir(IMAGES_DIR) if f.lower().endswith(SUPPORTED_FORMATS)]
    if not images:
        raise Exception("No images found in the images directory!")
    
    return os.path.join(IMAGES_DIR, random.choice(images))

def analyze_image(image_path):
    """Analyze the image and return a description"""
    try:
        # Generate image caption
        result = image_captioner(image_path)
        description = result[0]['generated_text']
        print(f"[{datetime.now()}] Image analysis: {description}")
        return description
    except Exception as e:
        print(f"[{datetime.now()}] Error analyzing image: {str(e)}")
        return None

def generate_caption(image_path):
    """Generate a unique caption based on image analysis using GPT"""
    # Get image description
    description = analyze_image(image_path)
    
    if not description:
        return "🌟 Load this in 4K for the full experience!"
    
    try:
        # Create a prompt for GPT
        prompt = f"""You are writing engaging captions for social media posts about a new feature that lets users click and hold to load images in 4K resolution.

The image shows: {description}

The tone should be casual, fun, and slightly trendy, appealing to users who are just discovering this feature.

Requirements:
- Keep it under 25 characters
- Must reference the click/hold to load 4K feature
- Make it feel like you're excited to show off this new feature
- Include at most 1 emoji (sometimes none)
- Reference the specific content of the image
- Sound natural and conversational
- No hashtags

Focus on making users want to try the new click-and-hold feature to see the image in 4K.

Generate a completely new caption:"""

        # Get completion from GPT
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a social media manager excited about launching a new image enhancement feature."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
            max_tokens=60
        )
        
        caption = response.choices[0].message.content.strip()
        print(f"[{datetime.now()}] Generated caption: {caption}")
        return caption
        
    except Exception as e:
        print(f"[{datetime.now()}] Error generating caption with GPT: {str(e)}")
        # Fallback to a basic caption
        return "🌟 Load this in 4K for the full experience!"

def process_image(image_path):
    """Process the image to ensure it meets X's requirements"""
    img = Image.open(image_path)
    
    # Create a temporary copy of the processed image
    temp_path = "temp_" + os.path.basename(image_path)
    
    # Get file size before processing
    original_size = os.path.getsize(image_path) / (1024 * 1024)  # Convert to MB
    print(f"[{datetime.now()}] Original image size: {original_size:.2f}MB")
    
    # Resize if the image is too large (X has a 5MB limit)
    max_size = (3840, 2160)  # 4K resolution
    img.thumbnail(max_size, Image.Resampling.LANCZOS)
    
    # Save processed image
    img.save(temp_path, "JPEG", quality=95)
    
    # Get file size after processing
    processed_size = os.path.getsize(temp_path) / (1024 * 1024)  # Convert to MB
    print(f"[{datetime.now()}] Processed image size: {processed_size:.2f}MB")
    
    return temp_path

def post_to_x():
    """Post an image to X with caption"""
    try:
        # Setup API clients
        client, api = setup_x_api()
        
        # Get and process image
        original_image_path = get_random_image()
        temp_image_path = process_image(original_image_path)
        
        try:
            # Upload media using v1.1 API
            print(f"[{datetime.now()}] Uploading image: {os.path.basename(original_image_path)}")
            media = api.media_upload(temp_image_path)
            
            # Generate caption
            caption = generate_caption(original_image_path)
            print(f"[{datetime.now()}] Posting tweet with caption: {caption}")
            
            # Try posting with v1.1 API first
            try:
                status = api.update_status(
                    status=caption,
                    media_ids=[media.media_id]
                )
                tweet_id = status.id
                print(f"[{datetime.now()}] Posted successfully using v1.1 API")
            except Exception as e1:
                print(f"[{datetime.now()}] v1.1 API posting failed, trying v2: {str(e1)}")
                # Fall back to v2 API if v1.1 fails
                response = client.create_tweet(
                    text=caption,
                    media_ids=[media.media_id]
                )
                tweet_id = response.data['id']
                print(f"[{datetime.now()}] Posted successfully using v2 API")
            
            print(f"[{datetime.now()}] Posted successfully: {os.path.basename(original_image_path)}")
            print(f"Tweet URL: https://twitter.com/i/web/status/{tweet_id}")
            
        finally:
            # Clean up temp file
            if os.path.exists(temp_image_path):
                os.remove(temp_image_path)
        
    except tweepy.TweepyException as e:
        print(f"[{datetime.now()}] Twitter API Error: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response Status: {e.response.status_code}")
            print(f"Response Text: {e.response.text}")
            
            # Additional error information
            if e.response.status_code == 403:
                print("\nPossible solutions for 403 Forbidden error:")
                print("1. Check if your Twitter Developer Account is active")
                print("2. Verify app permissions in Developer Portal:")
                print("   - Enable 'Read and Write' permissions")
                print("   - Regenerate tokens after permission changes")
                print("3. Check rate limits and account status")
                
    except Exception as e:
        print(f"[{datetime.now()}] Error: {str(e)}")

def main():
    """Main function to run the bot"""
    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)
        print(f"Created {IMAGES_DIR} directory. Please add your 4K images to this folder.")
        return
        
    images = [f for f in os.listdir(IMAGES_DIR) if f.lower().endswith(SUPPORTED_FORMATS)]
    if not images:
        print(f"No images found in {IMAGES_DIR}. Please add your 4K images and restart the bot.")
        return
        
    print("4K Tweet Bot Starting...")
    print(f"Found {len(images)} images in the images directory")
    print("Scheduled to post every 3 hours")
    
    # Post immediately on startup
    post_to_x()
    
    # Schedule future posts every 3 hours
    schedule.every(3).hours.do(post_to_x)
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
