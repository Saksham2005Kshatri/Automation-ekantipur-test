# Ekantipur News & Cartoon Scraper

A high-performance asynchronous web scraper built with **Python**, **Playwright**, and **uv**. This tool extracts the top 5 entertainment news stories and the "Cartoon of the Day" from [Ekantipur](https://ekantipur.com).

---

Ensure you have [uv](https://github.com/astral-sh/uv) installed.

1. **Install Playwright:**
   ```bash
   uv add playwright

2. **Install Browser Dependencies:**
   ```bash
   uv run playwright install chromium

3. **To run the code:**
   ```bash
   uv run python scraper.py
