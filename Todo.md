# Todo list

Here is a list of what I want to work on next.

## Todo Next

- Handle Selenium race condition when scraping a site.
  - See Selenium docs for info on this
~~- Add html parsing to get the jobs themselves.~~
  ~~- The html that can be scraped currently will have all the needed references for this. (Maybe use soup and requests. Verify if requests is sync or async)~~
- Add pytest tests for code
  - Specifically start with testing bad args?
  - Save several careers pages and test across all of them
- Improve error handling

## Bigger/Aspirational Todos
- Add multithreading to parse html as other pages are scraped.
- Add logging
- Add better page caching to avoid scraping urls every time the scraper runs.
- Publish as a python package

## Other potential additions
- Language support outside en-US
- Add scrapers for other sites (Greenhouse, etc...)
- Add generic scraper for easy custom implementation
- make a readthedocs.org page