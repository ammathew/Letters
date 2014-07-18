from xgoogle.search import GoogleSearch, SearchError
import time
import pickle


try:
    page = 1
    gs = GoogleSearch("shareholder letters")  
    gs.results_per_page = 100
    
    while page < 11:
        filename = 'urls_page_%s.txt'%(page)
        f = open( filename , 'w')
        print "page is"
        print page
        gs.page = page
        time.sleep(60)
        results = gs.get_results()
        urls = []
        for item in results:
            urls.append( item.url.encode("utf8") )   
        pickle.dump( urls, f )
        f.close()
        print "results count"
        print len( results )
        page += 1
except SearchError, e:
    print "Search failed: %s" % e




