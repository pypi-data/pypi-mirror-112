# DuckDuckGo Image Search API

DuckDuckGo Image Search API is a python application for programmatically downloading DuckDuckGo Image Search Results. This is for educational purposes only !
Forked from [https://github.com/deepanprabhu/duckduckgo-images-api](https://github.com/deepanprabhu/duckduckgo-images-api), I just updated it so it works with Python 3+

## Installation
```python
pip install duckduckgo-images-api
```
## Usage
```python
from duckduckgo_images_api import search
results = search("nike")
```
And `results` will have the following keys `ads, query, queryEncoded, response_type, results, vqd`.

To get the the image urls, run
```python
print([r["url"] for r in results["results"]])
```


## License
[MIT](https://choosealicense.com/licenses/mit/)

## Developer Connect
If you are a passionate developer looking to collaborate on interesting projects, feel free to connect through a PR in this project.
