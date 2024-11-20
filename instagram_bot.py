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
        
        # Initialize Chrome with WebDriver Manager
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Initialize SQLite database for follow tracking
        self.init_database()
        
    def init_database(self):
        """Initialize SQLite database to track follows"""
        import sqlite3
        
        self.db = sqlite3.connect('follow_tracker.db')
        cursor = self.db.cursor()
        
        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS follows (
                username TEXT PRIMARY KEY,
                followed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'pending'
            )
        ''')
        self.db.commit()
        
    def track_follow(self, username):
        """Record when we follow someone"""
        cursor = self.db.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO follows (username, followed_at, status)
            VALUES (?, CURRENT_TIMESTAMP, 'pending')
        ''', (username,))
        self.db.commit()
        
    def check_if_follows_back(self, username):
        """Check if a user follows us back"""
        try:
            # Go to their profile
            self.driver.get(f'https://www.instagram.com/{username}/')
            self.random_delay(2, 3)
            
            # Click on their followers list
            followers_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/followers')]"))
            )
            followers_button.click()
            self.random_delay(2, 3)
            
            # Search for our username in their followers
            try:
                our_username_element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((
                        By.XPATH, 
                        f"//div[@role='dialog']//a[contains(@href, '{self.username}')]"
                    ))
                )
                return True
            except:
                return False
                
        except Exception as e:
            print(f"Error checking if {username} follows back: {str(e)}")
            return False
            
    def unfollow_user(self, username):
        """Unfollow a specific user"""
        try:
            # Navigate to user's profile
            self.driver.get(f'https://www.instagram.com/{username}/')
            self.random_delay(2, 3)
            
            # Find and click unfollow button
            unfollow_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH, 
                    "//button[contains(text(), 'Following') or contains(text(), 'Requested')]"
                ))
            )
            unfollow_button.click()
            self.random_delay(1, 2)
            
            # Confirm unfollow if needed
            try:
                confirm_button = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((
                        By.XPATH, 
                        "//button[contains(text(), 'Unfollow') or contains(text(), 'Unfollow')]"
                    ))
                )
                confirm_button.click()
            except:
                pass  # No confirmation needed
                
            print(f"✓ Unfollowed {username}")
            return True
            
        except Exception as e:
            print(f"× Failed to unfollow {username}: {str(e)}")
            return False
            
    def cleanup_non_followers(self, hours=48):
        """Unfollow users who haven't followed back within specified hours"""
        cursor = self.db.cursor()
        
        # Get users who haven't followed back within the time limit
        cursor.execute('''
            SELECT username FROM follows 
            WHERE status = 'pending'
            AND datetime(followed_at, '+' || ? || ' hours') <= datetime('now')
        ''', (hours,))
        
        users_to_unfollow = cursor.fetchall()
        
        if not users_to_unfollow:
            print("No users to unfollow at this time")
            return
            
        print(f"\nChecking {len(users_to_unfollow)} users who haven't followed back...")
        
        for (username,) in users_to_unfollow:
            self.random_delay(30, 45)  # Delay between unfollows
            
            # Check if they follow us now
            if self.check_if_follows_back(username):
                cursor.execute('''
                    UPDATE follows SET status = 'follows_back'
                    WHERE username = ?
                ''', (username,))
                print(f"✓ {username} now follows back - keeping follow")
                continue
                
            # If they don't follow back, unfollow them
            if self.unfollow_user(username):
                cursor.execute('''
                    UPDATE follows SET status = 'unfollowed'
                    WHERE username = ?
                ''', (username,))
                
            self.db.commit()
        
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

    def follow_user(self, username):
        """Attempt to follow a single user with human-like behavior"""
        try:
            # Navigate to user's profile
            self.driver.get(f'https://www.instagram.com/{username}/')
            self.random_delay(3, 5)  # Increased initial delay
            
            # First check if the account exists/is accessible
            try:
                error_text = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Sorry')]"))
                )
                print(f"Cannot access {username}'s profile - account may be private or non-existent")
                return False
            except:
                pass  # No error message found, continue
            
            # Look for follow button with multiple possible XPaths
            follow_button = None
            button_xpaths = [
                "//button[contains(text(), 'Follow')]",
                "//button[contains(text(), 'Follow Back')]",
                "//div[contains(@class, 'x1i10hfl')]//button[contains(., 'Follow')]",
                "//button[@type='button' and not(contains(text(), 'Following')) and not(contains(text(), 'Requested'))]"
            ]
            
            for xpath in button_xpaths:
                try:
                    follow_button = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, xpath))
                    )
                    if follow_button and follow_button.is_displayed() and follow_button.is_enabled():
                        break
                except:
                    continue
            
            if not follow_button:
                print(f"Could not find follow button for {username}")
                return False
            
            # Check if already following or requested
            button_text = follow_button.text.lower()
            if 'following' in button_text or 'requested' in button_text:
                print(f"Already following or requested {username}")
                return False
            
            # Random delay before clicking
            self.random_delay(2, 4)
            
            # Try multiple click methods
            try:
                # Method 1: Regular click
                follow_button.click()
            except:
                try:
                    # Method 2: JavaScript click
                    self.driver.execute_script("arguments[0].click();", follow_button)
                except:
                    try:
                        # Method 3: Action chains
                        webdriver.ActionChains(self.driver)\
                            .move_to_element(follow_button)\
                            .click()\
                            .perform()
                    except Exception as e:
                        print(f"All click methods failed for {username}: {str(e)}")
                        return False
            
            # Verify the follow was successful
            self.random_delay(2, 3)
            try:
                # Check multiple possible button states
                verification_xpaths = [
                    "//button[contains(text(), 'Following')]",
                    "//button[contains(text(), 'Requested')]",
                    "//button[contains(@class, '_acan') and contains(text(), 'Following')]",
                    "//button[contains(@class, '_acan') and contains(text(), 'Requested')]",
                    "//div[contains(@class, '_aacl')]//button[contains(., 'Following')]",
                    "//div[contains(@class, '_aacl')]//button[contains(., 'Requested')]"
                ]
                
                for xpath in verification_xpaths:
                    try:
                        updated_button = WebDriverWait(self.driver, 2).until(
                            EC.presence_of_element_located((By.XPATH, xpath))
                        )
                        if updated_button:
                            print(f"✓ Successfully followed {username}")
                            return True
                    except:
                        continue
                
                # If we got here but the initial follow click worked, consider it a success
                print(f"✓ Follow action completed for {username} (status unverified)")
                return True
                
            except Exception as e:
                print(f"× Could not verify follow status for {username}, but action may have succeeded")
                return True  # Return True since the click worked
                
        except Exception as e:
            print(f"× Failed to follow {username}: {str(e)}")
            return False

    def follow_user_list(self, target_username):
        """Follow all users that a target account follows"""
        try:
            print(f"\nAccessing {target_username}'s profile...")
            self.driver.get(f'https://www.instagram.com/{target_username}/')
            self.random_delay(2, 4)
            
            # Get the following count
            following_count = self.get_following_count(target_username)
            
            # Click on following button
            following_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/following')]"))
            )
            following_button.click()
            self.random_delay()
            
            # Initialize counters
            successful_follows = 0
            failed_follows = 0
            follow_limit = 15  # Even more conservative limit
            consecutive_failures = 0
            max_consecutive_failures = 3
            
            # Scroll through the following list
            dialog = self.driver.find_element(By.XPATH, "//div[@role='dialog']")
            
            with tqdm(total=following_count, desc="Processing users") as pbar:
                prev_len = 0
                no_change_count = 0
                processed_users = set()
                
                while len(processed_users) < following_count and no_change_count < 3:
                    # Scroll and wait for new elements to load
                    self.driver.execute_script(
                        'arguments[0].scrollTop = arguments[0].scrollHeight;',
                        dialog
                    )
                    self.random_delay(1, 2)
                    
                    # Get all following usernames
                    following_elements = dialog.find_elements(By.XPATH, ".//a[@role='link']")
                    current_users = {
                        element.text for element in following_elements 
                        if element.text and not element.text.startswith('@')
                    }
                    
                    # Process new users
                    new_users = current_users - processed_users
                    for username in new_users:
                        if successful_follows >= follow_limit:
                            print(f"\nReached follow limit ({follow_limit}). Stopping for now.")
                            return successful_follows, failed_follows
                            
                        if consecutive_failures >= max_consecutive_failures:
                            print("\nToo many consecutive failures. Taking a longer break...")
                            self.random_delay(300, 600)  # 5-10 minute break
                            consecutive_failures = 0
                            
                        # Follow the user with a random delay
                        self.random_delay(45, 75)  # Increased delay between follows
                        if self.follow_user(username):
                            successful_follows += 1
                            consecutive_failures = 0
                        else:
                            failed_follows += 1
                            consecutive_failures += 1
                            
                    processed_users.update(new_users)
                    
                    # Update progress bar
                    new_items = len(processed_users) - prev_len
                    if new_items > 0:
                        pbar.update(new_items)
                        prev_len = len(processed_users)
                        no_change_count = 0
                    else:
                        no_change_count += 1
                        
            return successful_follows, failed_follows
            
        except Exception as e:
            print(f"\nError following users: {str(e)}")
            return 0, 0

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
                print("\nChoose an action:")
                print("1. Follow users from target account")
                print("2. Cleanup non-followers (48h)")
                print("3. Exit")
                
                choice = input("Enter your choice (1-3): ")
                
                if choice == "1":
                    target_username = input("\nEnter the target Instagram username: ")
                    successful, failed = bot.follow_user_list(target_username)
                    print(f"\nFollow operation completed:")
                    print(f"✓ Successfully followed: {successful} users")
                    print(f"× Failed to follow: {failed} users")
                    
                elif choice == "2":
                    bot.cleanup_non_followers(hours=48)
                    
                elif choice == "3":
                    break
                    
                if choice == "1":  # Add delay only after following operation
                    delay = random.randint(3600, 7200)  # 1-2 hour delay
                    print(f"\nWaiting {delay//3600} hours before next operation...")
                    time.sleep(delay)
                    
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        bot.close()

if __name__ == "__main__":
    main() 