import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
from pydantic import BaseModel

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific domains for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScrapeResponse(BaseModel):
    url: str
    detected_technologies: dict

# Function to set up Selenium WebDriver
def get_driver():
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/google-chrome-stable"  # Explicit Chrome binary path
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service("/usr/local/bin/chromedriver")  # Explicit ChromeDriver path
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def scrape_technologies(url: str):
    try:
        driver = get_driver()
        driver.get(url)
        time.sleep(5)
        page_source = driver.page_source
        driver.quit()

        soup = BeautifulSoup(page_source, "html.parser")
        detected_technologies = {}

        # Known tracking tools and analytics scripts
        technologies = {
              "Google Tag Manager": "googletagmanager.com",
    "Google Analytics": "analytics.js",
    "Google Analytics 4": "gtag/js",
    "Facebook Pixel": "connect.facebook.net/en_US/fbevents.js",
    "Hotjar": "static.hotjar.com",
    "Adobe Analytics": "omtrdc.net",
    "HubSpot": "js.hs-scripts.com",
    "LinkedIn Insight": "snap.licdn.com",
    "Twitter Pixel": "static.ads-twitter.com",
    "Segment.io": "cdn.segment.com",
    "Tealium": "tags.tiqcdn.com",
    "Piwik/Matomo": "matomo.js",
    "Crazy Egg": "script.crazyegg.com",
    "FullStory": "fullstory.com",
    "Microsoft Clarity": "clarity.ms",
    "Quantcast": "quantserve.com",
    "Chartbeat": "static.chartbeat.com",
    "New Relic": "js-agent.newrelic.com",
    "Kissmetrics": "doug1izaerwt3.cloudfront.net",
    "Mixpanel": "cdn.mxpnl.com",
    "Optimizely": "cdn.optimizely.com",
    "Pingdom": "rum-static.pingdom.net",
    "Smartlook": "rec.smartlook.com",
    "Yandex Metrica": "mc.yandex.ru",
    "VWO (Visual Website Optimizer)": "dev.visualwebsiteoptimizer.com",
    "Heap Analytics": "heap.io",
    "Mouseflow": "mouseflow.com",
    "Gauges": "secure.gaug.es",
    "Inspectlet": "inspectlet.com",
    "StatCounter": "statcounter.com",
    "Lucky Orange": "luckyorange.com",
    "Bing UET Tag": "bat.bing.com",
    "Flashtalking": "flashtalking.com",
    "DMP Lotame": "tags.crwdcntrl.net",
    "BlueKai": "tags.bluekai.com",
    "Everflow": "everflow.io",
    "AppsFlyer": "appsflyer.com",
    "Branch.io": "branch.io",
    "Adjust": "adjust.com",
    "AdRoll": "d.adroll.com",
    "Criteo": "criteo.com",
    "Taboola": "trc.taboola.com",
    "Outbrain": "widgets.outbrain.com",
    "Revcontent": "cdn.revcontent.com",
    "TripleLift": "ib.adnxs.com",
    "Google Ads Conversion Tracking": "googleadservices.com",
    "Google Floodlight": "fls.doubleclick.net",
    "Facebook Conversion API": "graph.facebook.com",
    "Snapchat Pixel": "sc-static.net",
    "TikTok Pixel": "analytics.tiktok.com",
    "Reddit Pixel": "events.reddit.com",
    "Quora Pixel": "q.quora.com",
    "Trade Desk": "insight.adsrvr.org",
    "LiveRamp": "idsync.rlcdn.com",
    "Oracle Data Cloud": "dmp.oracleservicecloud.com",
    "Lotame": "crwdcntrl.net",
    "Mediamath": "pixel.mathtag.com",
    "Sizmek": "bs.serving-sys.com",
    "Verizon Media": "s.yimg.com",
    
    # Demand-Side Platforms (DSPs)
    "Google Display & Video 360": "doubleclick.net",
    "The Trade Desk": "adsrvr.org",
    "Adform": "adform.net",
    "Xandr (formerly AppNexus)": "adnxs.com",
    "Amazon DSP": "amazon-adsystem.com",
    "StackAdapt": "stackadapt.com",
    "SmartyAds DSP": "smartyads.com",
    "Criteo Commerce Max": "criteo.com",
    "Yahoo! Advertising DSP": "yahoo.com",
    "MediaMath": "mathtag.com",
    "Basis DSP": "basis.net",
    "Demandbase Advertising": "demandbase.com",
    "EXADS": "exads.com",
    "Simpli.fi": "simpli.fi",
    "RTB House": "rtbhouse.com",
    "Beeswax (Owned by Comcast)": "beeswax.com",
    "Adobe Advertising Cloud": "adobe.com",
    "Moloco": "moloco.com",
    "Emerse": "emerse.com",
    "Taboola": "taboola.com",
    "Adelphic": "adelphic.com",
    "SiteScout": "sitescout.com",
    "Choozle": "choozle.com",
    "Rubicon Project": "rubiconproject.com",
    "iPinYou": "ipinyou.com",
    "Tradelab": "tradelab.com",
    "Pocketmath PRO": "pocketmath.com",
    "Centro Basis DSP": "basis.net",
    "eyeReturn": "eyereturn.com",
    "Turn": "turn.com",
    "Kritter": "kritter.in",
    "GetIntent": "getintent.com",
    "Byyd": "byyd.com",
    "MicroAd Blade": "microad.co.jp",
    "Taggify": "taggify.net",
    "TrafficAvenue": "trafficavenue.com",
    "MediaMath TerminalOne OS": "mediamath.com",
    "Bidease": "bidease.com",
    
    # Supply-Side Platforms (SSPs)
    "Google Ad Manager": "googlesyndication.com",
    "OpenX": "openx.net",
    "PubMatic": "pubmatic.com",
    "Magnite (formerly Rubicon Project)": "rubiconproject.com",
    "Index Exchange": "indexexchange.com",
    "Sovrn": "sovrn.com",
    "SpotX": "spotx.tv",
    "Teads": "teads.tv",
    "Xandr Monetize (formerly AppNexus)": "adnxs.com",
    "Amazon Publisher Services": "amazon-adsystem.com",
    "Sharethrough": "sharethrough.com",
    "Criteo": "criteo.com",
    "TripleLift": "triplelift.com",
    "Verizon Media": "verizonmedia.com",
    "Media.net": "media.net",
    "OpenX": "openx.com",
    "Adform": "adform.com",
    "Smaato": "smaato.com",
    "Improve Digital": "improvedigital.com",
    "Equativ (formerly Smart)": "smartadserver.com",
    "E-Planning": "e-planning.net",
    "GumGum": "gumgum.com",
    "Nativo": "nativo.com",
    "PulsePoint": "pulsepoint.com",
    "Sonobi": "sonobi.com",
        }

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
    return {"url": url, "detected_technologies": detected_technologies}

@app.get("/")
def home():
    return {"message": "API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
