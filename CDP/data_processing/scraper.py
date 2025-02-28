# data_processing/scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from annoy import AnnoyIndex
import os
import time

class CDPScraper:
    def __init__(self, cdps):
        self.cdps = cdps  # Dict of {'name': 'url'}
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.driver = self._init_selenium()
        
    def _init_selenium(self):
        options = Options()
        options.add_argument("--headless")  # Run in background
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(20)  # Timeout after 20 seconds
        return driver
    
    def scrape_docs(self):
        for cdp_name, url in self.cdps.items():
            print(f"Scraping {cdp_name}...")
            start_time = time.time()
            try:
                pages = self._get_all_pages(url)  # Scrape all pages
                chunks = []
                for page_url, content in pages.items():
                    chunks.extend(self.text_splitter.split_text(content))
                
                if not chunks:
                    print(f"No content found for {cdp_name}. Skipping...")
                    continue
                
                embeddings = self.model.encode(chunks)
                self._save_index(cdp_name, embeddings, chunks)
                print(f"Completed {cdp_name} in {time.time() - start_time:.2f} seconds.")
            except Exception as e:
                print(f"Failed to scrape {cdp_name}: {e}")
                continue
    
    def _get_all_pages(self, base_url):
        pages = {}
        try:
            # Navigate to the base URL
            self.driver.get(base_url)
            time.sleep(2)  # Wait for JavaScript to load
            
            # Extract all links from the page
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            links = soup.find_all('a', href=True)
            
            # Collect up to 5 documentation links to avoid infinite loops
            doc_links = []
            for link in links:
                href = link['href']
                if '/docs/' in href:  # Filter documentation links
                    if not href.startswith('http'):
                        href = base_url + href
                    doc_links.append(href)
                    if len(doc_links) >= 5:  # Limit to 5 pages for testing
                        break
            
            # Scrape each documentation page
            for doc_link in doc_links:
                content = self._scrape_page(doc_link)
                if content:
                    pages[doc_link] = content
        except TimeoutException:
            print(f"Timeout while loading {base_url}.")
        except WebDriverException as e:
            print(f"Selenium error: {e}")
        return pages
    
    def _scrape_page(self, url):
        try:
            self.driver.get(url)
            time.sleep(2)  # Wait for JavaScript
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            main_content = soup.find('main') or soup.find('article') or soup.find('body')
            if main_content:
                return main_content.get_text(separator=' ', strip=True)
        except Exception as e:
            print(f"Error scraping {url}: {e}")
        return None
    
    def _save_index(self, cdp_name, embeddings, chunks):
        if embeddings.shape[0] == 0:
            print(f"No embeddings generated for {cdp_name}. Skipping...")
            return
        
        embedding_dim = embeddings.shape[1]
        index = AnnoyIndex(embedding_dim, 'angular')
        for i, embedding in enumerate(embeddings):
            index.add_item(i, embedding)
        index.build(10)
        os.makedirs('indices', exist_ok=True)
        index.save(f'indices/{cdp_name}.ann')
        with open(f'indices/{cdp_name}_chunks.txt', 'w') as f:
            f.write('\n'.join(chunks))
    
    def close(self):
        """Explicitly close the WebDriver."""
        if self.driver:
            self.driver.quit()
            self.driver = None

if __name__ == "__main__":
    cdps = {
        "Segment": "https://segment.com/docs/?ref=nav",
        "mParticle": "https://docs.mparticle.com/",
        "Lytics": "https://docs.lytics.com/",
        "Zeotap": "https://docs.zeotap.com/home/en-us/"
    }
    scraper = CDPScraper(cdps)
    try:
        scraper.scrape_docs()
    finally:
        scraper.close()  # Ensure WebDriver is closed even if an error occurs
    print("Scraping and indexing completed!")
