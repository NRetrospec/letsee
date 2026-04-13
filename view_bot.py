import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os

# Configurable: Replace with target YouTube channel URL
CHANNEL_URL = 'https://www.youtube.com/@PhreshTeamTv/videos'

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def play_random_video(driver):
    try:
        driver.get(CHANNEL_URL)
        time.sleep(random.uniform(3, 7))
        
        # Better selector for video thumbnails on /videos tab
        video_thumbnails = driver.find_elements(By.CSS_SELECTOR, 'ytd-rich-item-renderer a#thumbnail')
        if not video_thumbnails:
            video_thumbnails = driver.find_elements(By.ID, 'thumbnail')
        
        if video_thumbnails:
            random_video = random.choice(video_thumbnails[:10])  # Limit to first 10 for speed
            driver.execute_script("arguments[0].click();", random_video)

            time.sleep(random.uniform(5, 10))
            
            # Play for random 1-5 min
            play_duration = random.randint(60, 300)
            print(f"Playing video for {play_duration//60} min...")
            time.sleep(play_duration)
            
            driver.back()
            time.sleep(random.uniform(3, 5))
        else:
            print("No videos found, retrying...")
            time.sleep(10)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(10)

def main():
    driver = None
    try:
        driver = setup_driver()
        while True:
            play_random_video(driver)
    except KeyboardInterrupt:
        print("View bot stopped.")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()

