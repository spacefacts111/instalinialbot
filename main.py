import random
import time
import requests
from playwright.sync_api import sync_playwright

# Your Instagram credentials (clearly embedded as requested)
INSTAGRAM_USERNAME = "knightinblindingarmour_"
INSTAGRAM_PASSWORD = "Joker800000"

# Your Gemini Web APIs (exactly like your Facebook bot)
GEMINI_IMAGE_API = "https://gemini-image-api.example.com/generate"
GEMINI_CAPTION_API = "https://gemini-caption-api.example.com/generate"

# Generate engaging, relatable philosophical captions
def generate_caption():
    prompt = ("Generate an engaging, relatable, mysterious and philosophical caption "
              "that matches a liminal space image. Keep it short and poetic.")
    
    response = requests.post(GEMINI_CAPTION_API, json={"prompt": prompt})
    response.raise_for_status()
    caption = response.json().get('caption')
    
    if not caption:
        caption = "In silent spaces, stories wait quietly."
    
    return caption.strip()

# Generate liminal space image from Gemini API
def generate_image():
    response = requests.get(GEMINI_IMAGE_API)
    response.raise_for_status()
    image_url = response.json().get('image_url')

    image_data = requests.get(image_url).content
    filename = 'image.jpg'
    with open(filename, 'wb') as file:
        file.write(image_data)
    return filename

# Post directly to Instagram using Playwright
def post_to_instagram(image_path, caption):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Login
        page.goto("https://www.instagram.com/accounts/login/")
        page.wait_for_selector('input[name="username"]', timeout=15000)
        page.fill('input[name="username"]', INSTAGRAM_USERNAME)
        page.fill('input[name="password"]', INSTAGRAM_PASSWORD)
        page.click('button[type="submit"]')
        page.wait_for_timeout(5000)

        # Navigate to posting interface
        page.goto("https://www.instagram.com/")
        page.wait_for_selector('svg[aria-label="New post"]', timeout=15000)
        page.click('svg[aria-label="New post"]')

        # Upload image
        page.wait_for_selector('input[type="file"]', timeout=15000)
        page.set_input_files('input[type="file"]', image_path)
        page.click('text=Next')
        page.wait_for_selector('textarea', timeout=15000)

        # Enter caption
        page.fill('textarea', caption)
        page.click('text=Share')
        page.wait_for_timeout(5000)

        context.close()
        browser.close()

# Automated posting routine (1–4 posts randomly per 24 hours)
def run_bot():
    posts_per_day = random.randint(1, 4)
    interval = (24 * 3600) // posts_per_day

    for _ in range(posts_per_day):
        image = generate_image()
        caption = generate_caption()
        post_to_instagram(image, caption)
        time.sleep(interval)

if __name__ == "__main__":
    run_bot()
