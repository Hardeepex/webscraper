# webscraper

# Instructions

## Using Docker for Selenium Grid

1. Build the Docker image for Selenium Grid:
   ```
   docker build -t selenium-grid .
   ```

2. Run the Docker image for Selenium Grid:
   ```
   docker run -d -p 4444:4444 --name selenium-grid selenium-grid
   ```
# To install the dependencies using pip and the requirements.txt file, run the following command:
# pip install -r requirements.txt

# To run the webscraper.py script, execute:
# python src/webscraper.py