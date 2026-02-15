from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

class APECScraper:
    def __init__(self, headless=False):
        """Initialise le scraper APEC"""
        self.driver = None
        self.headless = headless
        self.setup_driver()
    
    def setup_driver(self):
        """Configure le driver Chrome"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument('--headless')
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--start-maximized')
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
    
    def test_apec_connection(self):
        """Test simple : ouvrir APEC"""
        try:
            print("🔍 Ouverture d'APEC...")
            self.driver.get("https://www.apec.fr/")
            time.sleep(3)
            
            # Capturer le titre de la page
            title = self.driver.title
            print(f"✅ Page chargée : {title}")
            
            # Prendre une capture d'écran
            self.driver.save_screenshot("apec_test.png")
            print("📸 Capture d'écran sauvegardée : apec_test.png")
            
            return True
        except Exception as e:
            print(f"❌ Erreur : {e}")
            return False
    
    def close(self):
        """Ferme le navigateur"""
        if self.driver:
            input("Appuyez sur Entrée pour fermer le navigateur...")
            self.driver.quit()

# Test rapide
if __name__ == "__main__":
    print("=== TEST APEC SCRAPER ===\n")
    scraper = APECScraper(headless=False)
    scraper.test_apec_connection()
    scraper.close()
    