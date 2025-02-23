from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import time
from bs4 import BeautifulSoup
from pydantic import BaseModel

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific domains for better security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define response model
class ScrapeResponse(BaseModel):
    url: str
    detected_technologies: dict

# Function to set up Selenium WebDriver
def get_driver():
    chromedriver_autoinstaller.install()  # Auto-download ChromeDriver
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/google-chrome-stable"  # Explicitly set Chrome binary
    chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service("/usr/local/bin/chromedriver")  # Explicit ChromeDriver path
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Function to scrape technologies
def scrape_technologies(url: str):
    try:
        driver = get_driver()
        driver.get(url)
        time.sleep(5)  # Allow JavaScript to load fully
        page_source = driver.page_source
        driver.quit()

        soup = BeautifulSoup(page_source, "html.parser")
        detected_technologies = {}

        # Known tracking tools and analytics scripts
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Selenium error: {str(e)}")

@app.get("/scrape", response_model=ScrapeResponse)
def scrape(url: str):
    detected_technologies = scrape_technologies(url)
    return {
        "url": url,
        "detected_technologies": detected_technologies
    }

@app.get("/")
def home():
    return {"message": "API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
