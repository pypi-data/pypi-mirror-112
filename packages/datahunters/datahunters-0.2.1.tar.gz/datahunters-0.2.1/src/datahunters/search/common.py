"""Shared definition for search engine api.
"""

import abc
import json

from datahunters.shared.common import DataObjectBase


class ImgSearchResult(DataObjectBase):
  """Result object from image search.
  """
  thumbnail_url = None
  img_url = None
  link = None


class TextSearchResult(DataObjectBase):
  """Result object from text search.
  """
  title = ""
  link = None


class SearchEngineAPIBase(object):
  """Base class for search engine api.
  """
  __metaclass__ = abc.ABCMeta

  def __init__(self):
    pass

  def text_search(self, keywords):
    pass

  def img_search(self, keywords):
    pass
