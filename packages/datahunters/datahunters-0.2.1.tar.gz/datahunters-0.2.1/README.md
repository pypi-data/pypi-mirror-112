# DataHunters

DataHunters is an easy-to-use library to collect data from various sources, mainly designed for machine learning projects.

It contains modules of different types of data:

- search: search engine data, e.g. google, bing.
- social: social network, e.g. facebook, instagram, tinder.
- ecom: e-commerce data, e.g. products.
- movies: movie data.
- stock: stock image sites, e.g. unsplash, adobe stock.

## Installation

```
pip install datahunters
```

## Usage

Each data source usually have its specific data structure, you can find more in corresponding folder readme file.

As an example, let's say you want to collect images from google image search, you can simply do:

```python
from datahunters.search import google
```

## Contributing

If you have questions, comments, bug reports or adding new data sources, please create an issue or tweet at @flyfengjie.

## License

[MIT License](./LICENSE)