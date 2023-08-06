# psx-data-reader
with psx-data-reader, you can scrape the data of Pakistan stock exchange. psx-data-reader is super easy to use and handles everything for you. Just specify which company's stock data you want and how much you want, and the rest is done for you.

## Overview 
The psx-data-reader was written with fast use in mind. It provides the following key features

- can scrape all historical data till current date
- can scrape data for of multiple companies in a single line of code
- returns a `Pandas DataFrame` for the scraped data
- for better download speed, It does not request the complete data in a single network request rather it makes chunks of data to be downloaded and uses threads to open requests for different chunks of data, hence results in better speed

In the following paragraphs, I am going to describe how you can get and use Scrapeasy for your own projects.


## Installation

To get psx-data-reader, either fork this github repo or simply use Pypi via pip.

```bash
$ pip install psx-data-reader
```

## Usage

First, import stocks and tickers from psx

``
from psx import stocks, tickers
``

to get the information of all the companies in Pakistan stock Exchange....

```
tickers = tickers()
```


to scrape the data of **Silk Bank Limited** we have pass its ticker (symbol) to the `stocks` method with proper start and end date. and it will return a DataFrame with the scraped data

```
data = stocks("SILK", start=datetime.date(2020, 1, 1), datetime.today())
```


we can also download the data of multiple companies in a single call to `stocks` method by passing a list or tuple of symbols


```
data = stocks(["SILK", "PACE"], start=datetime.date(2020, 1, 1), datetime.today())
```

and now the returned DataFrame object will have a hierarchical index on rows.


## License
![GitHub](https://img.shields.io/github/license/MuhammadAmir5670/psx-data-reader)

## Author Info
<p align="left">
<a href="mailto:muhammmadamir5670@gmail.com"><img src="https://img.icons8.com/fluent/40/000000/gmail-new.png"/></a>
<a href = "https://www.linkedin.com/in/muhammad-amir-9826b71b5/"><img src="https://img.icons8.com/fluent/40/000000/linkedin.png"/></a>
<a href = "https://twitter.com/Daniyal60990408/"><img src="https://img.icons8.com/fluent/40/000000/twitter.png"/></a>
<a href="https://www.facebook.com/daniyal.abbasi.1610/">
<img src="https://img.icons8.com/fluent/40/000000/facebook-new.png">
</a>
<a href = "https://www.instagram.com/the_infamous_abbasi/"><img src="https://img.icons8.com/fluent/40/000000/instagram-new.png"/></a>
</p>

