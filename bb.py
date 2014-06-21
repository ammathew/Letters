from xgoogle.search import GoogleSearch, SearchError
try:
  gs = GoogleSearch("quick and dirty")
  gs.results_per_page = 50
  results = gs.get_results()
  for res in results:
      links.append( res.url.encode("utf8") )
  return results
except SearchError, e:
  print "Search failed: %s" % e
