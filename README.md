# Instagram Following Scraper Bot

A Python-based Instagram bot that helps you collect the list of accounts that a specific Instagram user follows. The bot uses Selenium WebDriver for automation and saves the results in JSON format.

## Features

- Automated Instagram login with secure credential handling
- Collects complete following list from any public Instagram profile
- Handles dynamic loading through scrolling
- Implements random delays to avoid rate limiting
- Saves results in JSON format
- Progress bar visualization during scraping
- Error handling and graceful exit
- Headless mode for background operation

## Prerequisites

Before running the bot, make sure you have:

- Python 3.7 or higher installed
- Google Chrome browser installed
- Required Python packages (see Installation section)
- Instagram account credentials

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/instagram-following-scraper-bot.git
```

2. Install required packages:

```bash
pip install selenium python-dotenv webdriver-manager tqdm
```

3. Create a `.env` file in the project root directory:

```bash
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_instagram_password
```

## Usage

1. Make sure your `.env` file is properly configured with your Instagram credentials

2. Run the script:

```bash
python instagram_bot.py
```

3. Enter the target Instagram username when prompted

4. The bot will save the following list in a JSON file named `{username}_following.json`

## How It Works

The bot:

1. Launches Chrome in headless mode
2. Logs into Instagram using your credentials
3. Navigates to the target user's profile
4. Opens their following list
5. Scrolls through the entire list
6. Saves all usernames to a JSON file

## Troubleshooting

If you encounter issues:

### Chrome Not Starting

- Update Chrome to the latest version
- Reinstall the required packages:

```bash
pip uninstall selenium webdriver-manager
pip install selenium webdriver-manager --upgrade
```

### Mac-Specific Issues

- Verify Chrome installation:

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version
```

- Add Chrome to PATH:

```bash
export PATH=$PATH:/Applications/Google\ Chrome.app/Contents/MacOS/
export PATH=$PATH:/usr/local/bin
```

### Windows-Specific Issues

- Verify Chrome is installed in the default location
- Try running without headless mode by commenting out:

```python
chrome_options.add_argument('--headless=new')
```

### Login Issues

- Check your credentials in the .env file
- Ensure your Instagram account is not locked
- Verify your internet connection

## Security Notes

⚠️ **Important Security Warnings:**

- Never commit your `.env` file to version control
- Always add `.env` to your `.gitignore` file
- Keep your Instagram credentials secure
- Change passwords immediately if accidentally committed
- Use this tool responsibly and ethically

## File Structure

- `instagram_bot.py`: Main script for scraping Instagram following
- `README.md`: This file, providing an overview, installation instructions, usage, and troubleshooting tips
- `.env`: Environment variables file for storing Instagram credentials
- `.gitignore`: File to exclude specific files from being tracked by Git

## Features Explained

### Headless Mode

The bot runs in headless mode by default, meaning it operates in the background without opening a visible browser window.

### Random Delays

Implements random delays between actions to mimic human behavior and avoid detection.

### Progress Bar

Shows real-time progress while collecting the following list.

### Error Handling

Comprehensive error handling for:

- Missing credentials
- Login failures
- Network issues
- Element loading timeouts

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This bot is for educational purposes only. Use it responsibly and in accordance with Instagram's terms of service. The developer is not responsible for any misuse or any resulting account restrictions.

## Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.
