"""API wrapper for news api.
"""

import datanews
from datahunters.news.base import Article, NewsAPIBase


def article_from_datanews_res(res_json):
  """Convert newsapi response to article object.
  """
  article = Article()
  article.title = res_json["title"]
  article.description = res_json["description"]
  article.author = ""
  for author in res_json["authors"]:
    if article.author == "":
      article.author = author
    else:
      article.author += ", " + author
  article.url = res_json["url"]
  article.cover_img_url = res_json["imageUrl"]
  article.publish_date = res_json["pubDate"]
  article.source = res_json["source"]
  return article


class DataNewsAPI(NewsAPIBase):
  """Class for data news.

  """
  API_KEY = "0admizneymdoi3y6cpwqd14o7"
  BASE_URL = "http://api.mediastack.com/v1/"

  def __init__(self):
    datanews.api_key = self.API_KEY

  def rate_limit_per_hour(self):
    return 10 / 24

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
    response = datanews.headlines(q=query,
                                  language=[language],
                                  topic=category,
                                  page=page,
                                  size=limit)
    articles = [article_from_datanews_res(x) for x in response["hits"]]
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
    response = datanews.news(q=query,
                             language=[language],
                             from_date=date_from,
                             to_date=date_to,
                             page=page,
                             size=limit)
    articles = [article_from_datanews_res(x) for x in response["hits"]]
    return articles


if __name__ == "__main__":
  api = DataNewsAPI()
  # articles = api.search_headlines("computer vision", category="tech", limit=10)
  articles = api.search_articles("computer vision",
                                 date_from="2021-01-31",
                                 limit=100)
  for article in articles:
    print(article.to_json())