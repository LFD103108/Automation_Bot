# Automated Library Book Renewal Bot

## Overview
This Python script automates the renewal of library books from the **UEL Virtual Library** using Selenium and BeautifulSoup. The script logs in to the user account, renews books if applicable, and retrieves due dates for future scheduling.
Acknowledgement to Arthur Souza Molina for the inspiration and help.

## Features
- **Automated Login**: Uses stored credentials to log into the library system.
- **Book Renewal**: Automatically selects and renews all borrowed books.
- **Due Date Extraction**: Retrieves the due date of each borrowed book.
- **Task Scheduling**: Uses Windows Task Scheduler to execute at the next due date.

## Requirements
Ensure you have the following installed:

- Python 3.x  
- Google Chrome Browser  
- ChromeDriver (installed automatically via `webdriver-manager`)  
- Required Python Libraries:

```sh
pip install selenium webdriver-manager beautifulsoup4
