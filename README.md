## Lead Generation Agent - Brief Overview

This application is an **AI-powered sales lead generator** that automatically finds and qualifies potential IT service clients in Vancouver, BC.

### What It Does:

1. **Searches for Local Businesses**: Uses web scraping to find 5 small businesses in Vancouver across various industries

2. **Gathers Intelligence**: For each business found, it:
   - Searches DuckDuckGo for detailed company information
   - Scrapes their websites to understand their operations
   - Analyzes their potential IT service needs

3. **Qualifies Leads**: Creates a structured report for each business including:
   - Company name
   - Contact information & email addresses
   - Summary of their potential IT needs
   - Personalized outreach message
   - Tools used in the research

4. **Saves Results**: Automatically saves all findings to a text file (`leads_output.txt`) with timestamps

### How It Works:

- **AI Agent**: Uses Mistral AI (or Gemini) to orchestrate the entire process
- **Custom Tools**: 
  - `search_web` - Searches the internet
  - `search_and_scrape` - Extracts website content
  - `save_to_txt` - Saves results to file
- **Structured Output**: Returns data in a clean JSON format that's easy to process

### Use Case:

Perfect for **IT service companies** or **sales teams** who need to:
- Quickly identify potential clients in a specific area
- Understand each prospect's business before reaching out
- Generate personalized outreach messages at scale
- Build a qualified lead list without manual research

**In essence**: It's an automated sales research assistant that does hours of manual work in minutes!
