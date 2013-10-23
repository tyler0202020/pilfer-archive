#--
#
# Name: pilfer-archive-new (attempt #2)
# Description: Pilfer Archive.org for files to fuzz. Fixed a few threading issues and organized the code better.
#              It still needs a little bit of work but thread stability is much better. glhf.
# Author(s): level@coresecurity.com
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. 
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, 
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT 
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR 
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGE.
#
#
#--



#--
#
# Name: pilfer-archive-new (attempt #2)
# Description: Pilfer Archive.org for files to fuzz. Fixed a few threading issues and organized the code better.
#              It still needs a little bit of work but thread stability is much better. glhf.
# Author(s): level@coresecurity.com
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. 
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, 
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT 
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR 
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGE.
#
#
#--



import re, urllib2, socket, json, os, Queue, sys
from threading import Thread

searchQueue,downloadQueue = Queue.Queue(),Queue.Queue()
log=True
debug=False

class Obtain:
	def file_exists(self,path):
		if (os.path.exists("repo/%s" % (path)) == True):
			return True
		else:
			return False
	def file_download(self,path):
		file = path.split("/")[-1]
		if (Obtain().file_exists(file) != True):
			data = urllib2.urlopen(path).read()
			if ("<html" not in data):
				fp = open("repo/%s" % (file),"w")
				fp.write(data)
				fp.close()
			if (log == True): print "[*] Wrote %s to file system" % (file)
		return

class Discover:
	def find_available(self,term):
		data = json.loads(urllib2.urlopen("https://archive.org/advancedsearch.php?q=%s&mediatype=&rows=1&page=1&output=json&save=no#raw" % (term)).read())
		numFound = data["response"]["numFound"]
		return numFound
	def get_titles(self,term,numFound):
		data = json.loads(urllib2.urlopen("https://archive.org/advancedsearch.php?q=%s&mediatype=&rows=%d&page=1&output=json&save=no#raw" % (term,numFound)).read())
		titles = []
		for i in xrange(0,numFound-1):
                        try:
                                if (" " in data["response"]["docs"][i]["title"]):
                                        titles.append(data["response"]["docs"][i]["title"].replace(" ","-"))
                                else:
                                        titles.append(data["response"]["docs"][i]["title"])
			except Exception as e:
                                pass
		return titles[:500]
	def get_locations(self,titles):
		urls = []
		for title in titles:
			try:
				data = json.loads(urllib2.urlopen("https://archive.org/details/%s&output=json&callback=IAE.favorite" % (title)).read()[13:-1])
				url = "https://%s%s" % (data["server"],data["dir"])
				urls.append(url)
			except Exception as e:
				if (debug == True): print "[*] DEBUG -- Function: Discover().get_locations('%s') Exception: %s" % (title,e)
				pass
		return urls[:500]
	def get_file_links(self,urls):
		files = {}
		for url in urls:
			data = urllib2.urlopen(url).read()
			files[url] = re.findall(r'href=[\'"]?([^\'" >]+)', data, re.UNICODE|re.MULTILINE)
			files[url] = files[url][1:]
		return files
		
		
class Queues:
	def search_worker(self):
		item = searchQueue.get()
		if (item != ""):
			numFound = Discover().find_available(item)
			if (log == True): print "[*] Found %d entries for %s" % (numFound,item)
			titles = Discover().get_titles(item,numFound)
			if (log == True): print "[*] Found %d titles for %s" % (len(titles),item)
			urls = Discover().get_locations(titles)
			if (log == True): print "[*] Found %d urls for %s" % (len(urls),item)
			files = Discover().get_file_links(urls)
			total = 0
			for url in files.iterkeys():
                                if (total >= 500):
                                        searchQueue.clear()
                                else:
                                        total+=len(files[url])
                                        for file in files[url]:
                                                downloadQueue.put("%s/%s" % (url,file))
                        if (log == True): print "[*] %d files for %s are in the download queue" % (total,item)
                	searchQueue.clear()
		return
	def download_worker(self):
                while True:
                        url = downloadQueue.get()
                        if (url != ""):
                                Obtain().file_download(url)
                        downloadQueue.task_done()
				
def main():
	#define file types
	itemz = ['3g2', '3gp', '3gp2', '3gpp', 'amv', 'asf', 'avi', 'bin', 'divx','drc','dv','f4v','flv','gxf','iso','m1v','m4v','m2t','m2v','mov','mp2','mp2v','mpa']
	#drop terms into queue
	for item in itemz:
		searchQueue.put(item)
	#create a bunch of queue threads
	for i in xrange(0,len(itemz)-1):
		t1 = Thread(target=Queues().search_worker(),name="search-%d" % (i)).start()
		t2 = Thread(target=Queues().download_worker(),name="download-%d" % (i)).start()
	sys.exit()

if __name__=="__main__":
	main()
