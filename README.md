# Instagram Follow Bot

An automated Instagram bot that helps manage following/unfollowing with smart tracking capabilities.

## Features

- Follow users from a target account's following list
- Track all followed accounts in a local database
- Automatically unfollow accounts that don't follow back after 48 hours
- Human-like behavior with random delays
- Conservative follow limits to avoid Instagram restrictions
- Visual Chrome browser for monitoring actions
- Progress bars for following operations

## Prerequisites

- Python 3.x
- Chrome browser installed
- Instagram account

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/instagram-auto-follow-bot.git
cd instagram-auto-follow-bot
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

4. The bot will:
   - Log into your Instagram account
   - Navigate to the target user's profile
   - Open their following list
   - Start following users with random delays
   - Stop after reaching the hourly limit (50 follows)
   - Wait 1-2 hours before processing another account

## Safety Features

The bot includes several safety measures to avoid Instagram restrictions:

- Follow limit: Maximum 50 follows per hour
- Random delays: 15-30 seconds between follows
- Session cooldown: 1-2 hour wait between accounts
- Human-like behavior: Random timing between actions
- Checks for existing follows before attempting to follow

## Troubleshooting

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

### Windows-Specific Issues

- Verify Chrome installation path
- Try running without headless mode by commenting out:

```python
chrome_options.add_argument('--headless=new')
```

### Follow Operation Issues

- Ensure target account is public
- Check if you've reached Instagram's follow limits
- Verify your account isn't restricted
- Check your internet connection

## Security Notes

⚠️ **Important Security Warnings:**

- Never commit your `.env` file to version control
- Always add `.env` to your `.gitignore` file
- Keep your Instagram credentials secure
- Use this tool responsibly to avoid account restrictions
- Follow Instagram's terms of service

## File Structure

```
instagram-auto-follow-bot/
├── instagram_bot.py     # Main bot script
├── .env                 # Environment variables (do not commit!)
├── .gitignore          # Git ignore file
└── README.md           # This file
```

## Operation Details

The bot follows these steps:

1. Launches Chrome in headless mode
2. Logs into Instagram using your credentials
3. Navigates to the target user's profile
4. Opens their following list
5. Follows users with random delays (15-30 seconds)
6. Stops after 50 follows
7. Waits 1-2 hours before processing another account

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This bot is for educational purposes only. Use it responsibly and in accordance with Instagram's terms of service. The developer is not responsible for any misuse or any resulting account restrictions.

⚠️ **Warning**: Following too many users too quickly can lead to account limitations or bans. Use this tool responsibly and at your own risk.

## Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.
