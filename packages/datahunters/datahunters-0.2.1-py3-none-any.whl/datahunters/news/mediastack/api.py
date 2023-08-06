"""API wrapper for news api.
"""

import requests
from datahunters.news.base import Article, NewsAPIBase


def article_from_mediastack_res(res_json):
  """Convert newsapi response to article object.
  """
  article = Article()
  article.title = res_json["title"]
  article.description = res_json["description"]
  article.author = res_json["author"]
  article.url = res_json["url"]
  article.cover_img_url = res_json["image"]
  article.publish_date = res_json["published_at"]
  article.source = res_json["source"]
  return article


class MediaStackAPI(NewsAPIBase):
  """Class for media stack.

  """
  API_KEY = "310e0c269d59aa84e7f750d92cdab25e"
  BASE_URL = "http://api.mediastack.com/v1/"

  def __init__(self):
    pass

  def rate_limit_per_hour(self):
    return 500 / 31 / 24

  def search_headlines(self,
                       query,
                       sources=None,
                       category=None,
                       language="en",
                       country="us",
                       limit=50,
                       page=1):
    """Retrieve headlines.
    """
    req_url = "{}news?access_key={}&keywords={}".format(
        self.BASE_URL, self.API_KEY, query)
    if sources:
      req_url += "&sources={}".format(sources)
    if category:
      req_url += "&categories={}".format(category)
    if language:
      req_url += "&languages={}".format(language)
    if country:
      req_url += "&countries={}".format(country)
    req_url += "&limit={}&offset={}".format(limit, page)
    res = requests.get(req_url)
    res_json = res.json()
    articles = [article_from_mediastack_res(x) for x in res_json["data"]]
    return articles

  def search_articles(self,
                      query,
                      sources=None,
                      date_from=None,
                      date_to=None,
                      language="en",
                      country="us",
                      limit=100,
                      page=1,
                      sort_by="publishedAt"):
    """Retrieve articles.
    """
    req_url = "{}news?access_key={}&keywords={}".format(
        self.BASE_URL, self.API_KEY, query)
    if sources:
      req_url += "&sources={}".format(sources)
    if language:
      req_url += "&languages={}".format(language)
    if country:
      req_url += "&countries={}".format(country)
    if date_from and date_to:
      req_url += "&date={},{}".format(date_from, date_to)
    req_url += "&limit={}&offset={}".format(limit, page)
    res = requests.get(req_url)
    res_json = res.json()
    articles = [article_from_mediastack_res(x) for x in res_json["data"]]
    return articles


if __name__ == "__main__":
  api = MediaStackAPI()
  # articles = api.search_headlines("computer vision",
  #                                 category="technology",
  #                                 limit=10)
  articles = api.search_articles("computer vision", limit=10)
  for article in articles:
    print(article.to_json())