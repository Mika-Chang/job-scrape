import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class WorkdayScraper:
    """Class to scrape a workday careers page."""

    def __init__(self, driver:webdriver=None):
        """Initialize scraper.
        
        Parameters
        ----------
        driver : selenium.webdriver, default=None
            The webdriver to scrape the site.
        """
        if driver == None:
            # TODO make sure chrome driver works too
            service = webdriver.FirefoxService()
            self.__driver = webdriver.Firefox(service=service)
        else:
            self.__driver = driver

    def __get_next_page_class(self, soup:BeautifulSoup):
        """Get the css class of the next button.
        
        Parameters
        ----------
        soup : bs4.BeautifulSoup
            A beautiful soup object created from the html page to search for a next button
        
        Returns
        -------
        str
            The class used for the next button or an empty string if there is no next button.
        """
        # Get the nav elements responsible for controlling the page
        for nav in soup.find_all("nav", attrs={"aria-label": "pagination"}):
            # Check all buttons for a next button
            for button in nav.find_all('button'):
                if button.has_attr('aria-label') and button["aria-label"] == "next":
                    if button.has_attr('class'):
                        return button['class'][0]
        return ''
    
    def __next_page(self, css_class:str):
        """Move to the next page of jobs.
        
        Parameters
        ----------
        css_class : str
            The css class of the next button.

        Raises
        ------
        ValueError
            If there is no next button associated with the specified css class.
        """
        # Move to the next page if it exists
        page_nav_elements = self.__driver.find_elements(
            By.CSS_SELECTOR, '.' + css_class)
        time.sleep(3)
        for element in page_nav_elements:
            # This check needed because previous and next buttons have the same class
            if element.get_attribute("aria-label") == "next":
                element.click()
                return
        raise ValueError('Next button specified but not found')

    def scrape(self, url:str, cache_path:str=None):
        """Scrape all pages of a specified workday site.
        
        Parameters
        ----------
        url : str
            The url of the site to scrape.
        cache_path : str, default=None
            The path of the directory to store the scaped html pages.
        """
        page_count = 0

        self.__driver.get(url)
        while True:
            next_class = None
            time.sleep(3) # TODO implement better wait strategy
            # get page html
            html = self.__driver.page_source
            soup = BeautifulSoup(html, features="html.parser")
            page_count += 1

            # save current page
            if cache_path != None:
                with open (
                        os.path.join(cache_path, f'p{page_count}.html'), 
                        'w+', encoding='utf-8') as f:
                    f.write(html)

            # TODO potentially parse html here. 

            # check for / navigate to next page
            next_class = self.__get_next_page_class(soup)
            if next_class != '':
                self.__next_page(next_class)
            else:
                print("No next button detected. Scraping complete")
                print(f"Scraped {page_count} pages.")
                break

    def close_driver(self):
        """Close the webdriver used by the scraper."""
        self.__driver.close()