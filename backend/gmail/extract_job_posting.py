import re
from bs4 import BeautifulSoup
import httpx
from playwright.sync_api import sync_playwright
from pathlib import Path

def extract_seek_job_url(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    seek_link_pattern = re.compile(r'^https://email\.s\.seek\.com\.au/uni/ss/c')

    links = soup.find_all(
        'a',
        href = seek_link_pattern,
        style=lambda s:s and 'display: block' in s.lower()
    )

    if links:
        print(links[0]['href'])
        return links[0]['href']
    return None



def job_posting_to_pdf(email_id, link, output_folder):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    with httpx.Client(follow_redirects = True, headers = headers) as client:
        response = client.get(link)
        final_url = str(response.url)
        print(f'Resolved target url: {final_url}')

    with sync_playwright() as p:
        browser = p.chromium.launch(headless = True)

        page = browser.new_page()
        
        page.goto(final_url, wait_until = "domcontentloaded", timeout=60000)
        
        page.wait_for_selector('h1', timeout=10000)

        page.pdf(
            path = file,
            format = "A4",
            print_background = True,
            margin = {
                "top" : "0.04in",
                "bottom" : "0.04in",
                "left" : "0.04in",
                "right" : "0.04in"
            }
        )

        browser.close()
    print(f'Saved job posting as {file}')