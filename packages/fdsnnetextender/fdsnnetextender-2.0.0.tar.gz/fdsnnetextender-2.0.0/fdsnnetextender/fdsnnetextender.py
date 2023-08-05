from functools import lru_cache
from urllib.request import urlopen
import re
import logging

class FdsnNetExtender():
  """
  Toolbox to manage the correspondance between a short network code and an extended network code.
  Correspondance is made using the metadata
  """
  def __init__(self, base_url="eida-federator.ethz.ch"):
    """
    param: base_url is the base url for getting metadata. Default is ws.
    """
    # we can guess that a network is temporary from this regex:
    self.tempo_network_re = '^[0-9XYZ][0-9A-Z]$'
    self.base_url = base_url

  @lru_cache(maxsize=1000)
  def extend(self, net, year):
    """
    Given a short code and a year
    Returns the corresponding extended network code for temporary networks
    """
    logging.debug("Trying to extend %s for %s", net, year)
    extnet = net
    # Only extend temporary networks
    if re.match(self.tempo_network_re, net):
      request = f"http://{self.base_url}/fdsnws/station/1/query?format=text&level=network&net={net}&startbefore={year}-12-31&endafter={year}-01-01"
      try:
        with urlopen(request) as metadata:
          if metadata.status == 200:
            extnet = net + metadata.readlines()[1].decode('utf-8').split('|')[-3][0:4]
          elif metadata.status == 204:
            raise ValueError(f"No metadata for request {request}")
      except Exception as e:
          logging.error(e)
          raise e
    return extnet
