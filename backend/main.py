from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScrapeResponse(BaseModel):
    url: str
    detected_technologies: dict

# Set up Selenium WebDriver
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def scrape_technologies(url: str):
    driver = get_driver()
    driver.get(url)
    time.sleep(5)  # Wait for JavaScript content to load
    page_source = driver.page_source  # Get the fully loaded HTML
    driver.quit()

    soup = BeautifulSoup(page_source, "html.parser")
    detected_technologies = {}

    technologies = {
        "Google Tag Manager": "googletagmanager.com",
        "Google Analytics": "analytics.js",
        "Facebook Pixel": "connect.facebook.net/en_US/fbevents.js",
        "Hotjar": "static.hotjar.com",
        "Adobe Analytics": "omtrdc.net",
        "HubSpot": "js.hs-scripts.com",
        "LinkedIn Insight": "snap.licdn.com",
        "Twitter Pixel": "static.ads-twitter.com",
        "Segment.io": "cdn.segment.com",
        "Tealium": "tags.tiqcdn.com",
    }

    # Check for technologies in the rendered HTML
    for script in soup.find_all("script", src=True):
        script_src = script["src"]
        for tech, keyword in technologies.items():
            if keyword in script_src:
                detected_technologies[tech] = "Detected"

    return detected_technologies

@app.get("/scrape", response_model=ScrapeResponse)
def scrape(url: str):
    detected_technologies = scrape_technologies(url)
    return {"url": url, "detected_technologies": detected_technologies}

@app.get("/")
def home():
    return {"message": "API is running!"}
