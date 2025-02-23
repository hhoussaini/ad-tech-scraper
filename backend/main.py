from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace "*" with your frontend URL for better security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScrapeResponse(BaseModel):
    url: str
    detected_technologies: dict

def scrape_technologies(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)  # 10s timeout
        response.raise_for_status()  # Raise error if HTTP request fails
        
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

        # Check for technologies in the raw HTML
        for tech, keyword in technologies.items():
            if keyword in response.text:
                detected_technologies[tech] = "Detected"

        return detected_technologies

    except requests.exceptions.Timeout:
        return {"error": "Request timed out"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}

@app.get("/scrape", response_model=ScrapeResponse)
def scrape(url: str):
    detected_technologies = scrape_technologies(url)
    return {"url": url, "detected_technologies": detected_technologies}

@app.get("/")
def home():
    return {"message": "API is running!"}
