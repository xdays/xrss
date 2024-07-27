# Introduction

Automatically fetch blog updates and send them out via email.

# Functional Modules

- Parse the blog's RSS feed.
- Populate a template to generate HTML content.
- Send the generated HTML to Gmail.
- Log activities throughout the process.

# Configuration File Overview

## Email Configuration

- addresser: sender's email address
- password: sender's password

## Main Program Configuration

- template_dir: template directory
- template_file: template file name
- stale_date: expiration date for logs
- urls: list of RSS sources
- recipients: list of recipients

## Logging Configuration

Standard Python logging module configuration.

# Module List

- ConfigParser
- logging
- logging.config
- feedparser
- datetime
- mailer
- jinja2

# Usage

```bash
pip install -r requirements.txt
python3 main.py
```

# Tools

## extractrss.py

Used to extract RSS feed links from web pages.
