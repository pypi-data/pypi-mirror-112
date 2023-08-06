"""Google api class.
"""

import urllib

from datahunters.shared.selenium_scraper import SeleniumScraper
from datahunters.search.common import ImgSearchResult


class GoogleSearchAPI(SeleniumScraper):
  """Class for google image search api.
  """
  base_url = "https://www.google.com/search"

  def __init__(self, use_headless=True):
    super().__init__(use_headless)
    print("Google image api initialized")

  def convert_elem_to_obj(self, elem):
    """Convert page element to image object.
    """
    cur_res = ImgSearchResult()
    # src = elem.get_attribute("src")
    # if src is None:
    #   print(elem.get_attribute("innerHTML"))
    link = self.get_attribute_values([elem], "src")[0]
    link = urllib.parse.unquote(link)
    cur_res.img_url = link
    # load image detail page.
    # self.load_content(link)
    # elems = self.find_elements("img.n3VNCb")
    # if elems:
    #   elem = elems[0]
    #   link = self.get_attribute_values([elem], "src")[0]
    #   cur_res.img_url = link
    # cur_res.img_url = link[link.find("imgurl=") +
    #                        7:link.find("&imgrefurl")].rstrip(".")
    return cur_res

  def img_search(self, keywords, get_all=False):
    """Collect images from google search results.

    Args:
      keywords: search input.
      item_num: number of items to retrieve.
      get_all: if get all available results or just first page.

    Returns:
      list of image items.
    """
    all_res = []
    try:
      print("start scraping '{}' using Google".format(keywords))
      formatted_keywords = keywords.strip().replace(" ", "+")
      req_url = "{}?q={}&source=lnms&tbm=isch&sa=X&ei=0eZEVbj3IJG5uATalICQAQ&ved=0CAcQ_AUoAQ&biw=939&bih=591".format(
          self.base_url, formatted_keywords)
      print(req_url)
      # check default page.
      print("checking default data")
      if not get_all:
        self.load_content(req_url, "img.rg_i")
        # source = self.browser.page_source
        # with open("./source.txt", "w") as f:
        #   f.write(source)
        # exit(0)
        elems = self.find_elements("img.rg_i")
      else:
        elems = self.scrape_inf_scroll(req_url,
                                       "a.rg_i",
                                       None,
                                       load_btn_selector="input#smb")
      print("total fetched items: {}".format(len(elems)))
      for elem in elems:
        try:
          cur_res = self.convert_elem_to_obj(elem)
          all_res.append(cur_res)
        except Exception as ex:
          print("error in processing item: {}".format(ex))
          continue
      print("Google image scraping finished.")
      return all_res
    except Exception as ex:
      print("error in Google image scraper: {}".format(ex))
      return all_res


if __name__ == "__main__":
  engine = GoogleSearchAPI()
  all_imgs = engine.img_search("cats", False)
  print(len(all_imgs))