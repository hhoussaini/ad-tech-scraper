from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your frontend URL for better security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScrapeResponse(BaseModel):
    url: str
    detected_technologies: dict

def scrape_technologies(url: str):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    detected_technologies = {}

    # List of known scripts and tracking tools
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

    # Check script tags for known tracking technologies
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
