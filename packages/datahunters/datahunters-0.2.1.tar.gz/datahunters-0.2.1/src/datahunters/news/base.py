"""Base classes for news api category.
"""

import abc
import json

from datahunters.shared.common import DataObjectBase


class Article(DataObjectBase):
  """Base class for article.
  """
  title = ""
  description = ""
  author = ""
  url = ""
  cover_img_url = ""
  author = ""
  source = ""
  publish_date = ""


class NewsAPIBase(abc.ABC):
  """Base class for news related apis.
  """
  def rate_limit_per_hour(self):
    pass

  def search_headlines(self, query, sources, category, language, country,
                       limit, page):
    pass

  def search_articles(self, query, sources, date_from, date_to, language,
                      country, limit, page, sort_by):
    pass