"""API wrapper for news api.
"""

import requests
from datahunters.news.base import Article, NewsAPIBase


def article_from_gnews_res(res_json):
  """Convert gnews response to article object.
  """
  article = Article()
  article.title = res_json["title"]
  article.description = res_json["description"]
  article.author = res_json["source"]["name"]
  article.url = res_json["url"]
  article.cover_img_url = res_json["image"]
  article.publish_date = res_json["publishedAt"]
  article.source = res_json["source"]["name"]
  return article


class GNewsAPI(NewsAPIBase):
  """Class for gnews.
  https://gnews.io/

  """
  API_KEY = "9bf2f28f1051d476b53f4075308a38ea"
  BASE_URL = "https://gnews.io/api/v4/"

  def __init__(self):
    pass

  def rate_limit_per_hour(self):
    return 100 / 24

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
    req_url = "{}top-headlines?token={}&q={}".format(self.BASE_URL,
                                                     self.API_KEY, query)
    if category:
      req_url += "&topic={}".format(category)
    if language:
      req_url += "&lang={}".format(language)
    req_url += "&limit={}&offset={}".format(limit, page)
    res = requests.get(req_url)
    res_json = res.json()
    articles = [article_from_gnews_res(x) for x in res_json["articles"]]
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
    req_url = "{}search?token={}&q={}".format(self.BASE_URL, self.API_KEY,
                                              query)
    if language:
      req_url += "&lang={}".format(language)
    # if country:
    #   req_url += "&country={}".format(country)
    if date_from and date_to:
      req_url += "&from={}&to={}".format(date_from, date_to)
    req_url += "&max={}&page={}".format(limit, page)
    res = requests.get(req_url)
    res_json = res.json()
    articles = [article_from_gnews_res(x) for x in res_json["articles"]]
    return articles


if __name__ == "__main__":
  api = GNewsAPI()
  # articles = api.search_headlines("computer vision",
  #                                 category="technology",
  #                                 limit=10)
  articles = api.search_articles("computer vision", limit=10)
  for article in articles:
    print(article.to_json())