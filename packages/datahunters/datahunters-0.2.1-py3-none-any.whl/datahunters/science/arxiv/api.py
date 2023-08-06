"""arXiv api.

https://arxiv.org/help/api
"""

import requests
import atoma
import json


class arXivAPI(object):
  """Class of arXiv api.
  """
  def __init__(self):
    self.API_URL = "http://export.arxiv.org/api"

  def search(self, title_query, field, num_results=10):
    """Search for publications.

    Args:
      title_query: query keywords used in title.
      field: subject field code, https://arxiv.org/help/api/user-manual#Architecture.
      num_results: number of items to return. get all by setting -1.
    """
    items = []
    for start_id in range(0, num_results, 10):
      max_results = 10 if num_results - start_id >= 10 else num_results - start_id
      req_url = "{}/query?search_query=ti:{}+AND+cat:{}&start={}&max_results={}&sortBy=submittedDate&sortOrder=descending".format(
          self.API_URL, title_query, field, start_id, max_results)
      res = requests.get(req_url)
      feed = atoma.parse_atom_bytes(res.content)
      # parse results into items.
      for entry in feed.entries:
        item = {}
        item["title"] = entry.title.value
        item["authors"] = [author.name for author in entry.authors]
        item["links"] = [(link.href, link.title) for link in entry.links]
        item["publish_date"] = entry.published.isoformat()
        item["update_date"] = entry.updated.isoformat()
        item["summary"] = entry.summary.value
        item["categories"] = [category.term for category in entry.categories]
        items.append(item)
    return items


if __name__ == "__main__":
  # quick test.
  api = arXivAPI()
  items = api.search("dataset", "cs.CV", 23)
  with open("./test.json", "w") as f:
    json.dump(items, f)
