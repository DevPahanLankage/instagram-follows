# Add these at the very top of the file, before any imports
print("Script starting...")
print("Importing modules...")

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import json
import os
import random
from dotenv import load_dotenv
from tqdm import tqdm
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

print("Modules imported successfully")

class InstagramBot:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        self.username = os.getenv('INSTAGRAM_USERNAME')
        self.password = os.getenv('INSTAGRAM_PASSWORD')
        
        # Check if credentials are loaded
        if not self.username or not self.password:
            raise ValueError(
                "Missing Instagram credentials. Please check your .env file contains:\n"
                "INSTAGRAM_USERNAME=your_username\n"
                "INSTAGRAM_PASSWORD=your_password"
            )
        
        # Add options for better performance
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--disable-popup-blocking')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--headless=new')
        
        # Initialize Chrome with WebDriver Manager
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
    def random_delay(self, min_delay=1, max_delay=3):
        time.sleep(random.uniform(min_delay, max_delay))
        
    def login(self):
        try:
            print("Logging in to Instagram...")
            self.driver.get('https://www.instagram.com/accounts/login/')
            self.random_delay()
            
            # Handle cookie consent if it appears
            try:
                cookie_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'Allow')]")
                cookie_button.click()
                self.random_delay()
            except:
                pass
            
            # Enter username
            username_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_input.send_keys(self.username)
            self.random_delay(0.5, 1.5)
            
            # Enter password
            password_input = self.driver.find_element(By.NAME, "password")
            password_input.send_keys(self.password)
            self.random_delay(0.5, 1.5)
            
            # Click login button
            password_input.send_keys(Keys.RETURN)
            self.random_delay(3, 5)
            
            # Check for login success
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/direct/inbox')]"))
                )
                print("Login successful!")
                return True
            except:
                print("Login verification failed. Please check your credentials.")
                return False
                
        except Exception as e:
            print(f"Login failed: {str(e)}")
            return False
            
    def get_following_count(self, target_username):
        try:
            following_count_element = self.driver.find_element(
                By.XPATH, 
                "//a[contains(@href, '/following')]/span/span"
            )
            return int(following_count_element.text.replace(',', ''))
        except:
            return 100  # Default value if count cannot be determined
            
    def get_following_list(self, target_username):
        try:
            print(f"\nAccessing {target_username}'s profile...")
            self.driver.get(f'https://www.instagram.com/{target_username}/')
            self.random_delay(2, 4)
            
            # Get the following count to determine scroll iterations
            following_count = self.get_following_count(target_username)
            
            # Click on following button
            following_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/following')]"))
            )
            following_button.click()
            self.random_delay()
            
            # Scroll through the following list
            following_list = set()  # Using set to avoid duplicates
            dialog = self.driver.find_element(By.XPATH, "//div[@role='dialog']")
            
            with tqdm(total=following_count, desc="Collecting followings") as pbar:
                prev_len = 0
                no_change_count = 0
                
                while len(following_list) < following_count and no_change_count < 3:
                    # Scroll and wait for new elements to load
                    self.driver.execute_script(
                        'arguments[0].scrollTop = arguments[0].scrollHeight;',
                        dialog
                    )
                    self.random_delay(1, 2)
                    
                    # Get all following usernames
                    following_elements = dialog.find_elements(By.XPATH, ".//a[@role='link']")
                    current_following_list = {
                        element.text for element in following_elements 
                        if element.text and not element.text.startswith('@')
                    }
                    
                    following_list.update(current_following_list)
                    
                    # Update progress bar
                    new_items = len(following_list) - prev_len
                    if new_items > 0:
                        pbar.update(new_items)
                        prev_len = len(following_list)
                        no_change_count = 0
                    else:
                        no_change_count += 1
                    
            return list(following_list)
            
        except Exception as e:
            print(f"\nError getting following list: {str(e)}")
            return []
            
    def close(self):
        print("\nClosing browser...")
        self.driver.quit()

def main():
    print("Initializing bot...")
    try:
        bot = InstagramBot()
    except ValueError as e:
        print(f"Error: {e}")
        return
    except Exception as e:
        print(f"Failed to initialize bot: {e}")
        return

    try:
        if bot.login():
            while True:
                target_username = input("\nEnter the target Instagram username (or 'quit' to exit): ")
                
                if target_username.lower() == 'quit':
                    break
                    
                following_list = bot.get_following_list(target_username)
                
                if following_list:
                    # Save results to a file
                    filename = f'{target_username}_following.json'
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(following_list, f, indent=4, ensure_ascii=False)
                        
                    print(f"\nFound {len(following_list)} accounts that {target_username} is following")
                    print(f"Results have been saved to {filename}")
                else:
                    print(f"\nCouldn't retrieve following list for {target_username}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        bot.close()

if __name__ == "__main__":
    main() 