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
debug=True

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
		data = json.loads(urllib2.urlopen("http://archive.org/advancedsearch.php?q=%s&mediatype=&rows=1&page=1&output=json&save=no#raw" % (term)).read())
		numFound = data["response"]["numFound"]
		return numFound
	def get_titles(self,term,numFound):
		data = json.loads(urllib2.urlopen("http://archive.org/advancedsearch.php?q=%s&mediatype=&rows=%d&page=1&output=json&save=no#raw" % (term,numFound)).read())
		titles = []
		for i in xrange(0,numFound-1):
			if (" " in data["response"]["docs"][i]["title"]):
				titles.append(data["response"]["docs"][i]["title"].replace(" ","-"))
			else:
				titles.append(data["response"]["docs"][i]["title"])
		return titles
	def get_locations(self,titles):
		urls = []
		for title in titles:
			try:
				data = json.loads(urllib2.urlopen("http://archive.org/details/%s&output=json&callback=IAE.favorite" % (title)).read()[13:-1])
				url = "http://%s%s" % (data["server"],data["dir"])
				urls.append(url)
			except Exception as e:
				if (debug == True): print "[*] DEBUG -- Function: Discover().get_locations('%s') Exception: %s" % (title,e)
				pass
		return urls
	def get_file_links(self,urls):
		files = {}
		for url in urls:
			data = urllib2.urlopen(url).read()
			files[url] = re.findall(r'href=[\'"]?([^\'" >]+)', data, re.UNICODE|re.MULTILINE)
			files[url] = files[url][1:]
		return files
		
		
class Queues:
	def search_worker(self):
		while True:
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
					total+=len(files[url])
					if (log == True): print "[*] Found %d files" % (total)
					for file in files[url]:
						downloadQueue.put("%s/%s" % (url,file))
					if (log == True): print "[*] Added %d files for %s to the download queue" % (total,item)
				searchQueue.task_done()
			break
		return
	def download_worker(self):
		while True:
			url = downloadQueue.get()
			if (url != ""):
				Obtain().file_download(url)
			downloadQueue.task_done()
			break
		return
				
def main():
	#define file types
	# itemz = ['xcf', 'pix', 'matte', 'mask', 'alpha', 'fli', 'flc', 'xcf.bz2', 'xcfbz2', 'desktop', 
	# 'dcm', 'dicom', 'eps', 'fit', 'fits', 'g3', 'gif', 'gbr', 'gpb', 'gih', 'pat', 'xcf.gz', 'xcfgz', 
	# 'jp2', 'jpc', 'jpx', 'j2k', 'jpg', 'jpeg', 'jpe', 'cel', 'ico', 'wmf', 'apm', 'ora', 'psp', 'tub', 
	# 'pspimage', 'psd', 'png', 'pnm', 'ppm', 'pgm', 'pbm', 'png', 'pnm', 'ppm', 'pgm', 'pbm', 'pdf', 'ps', 
	# 'data', 'sgi','rgb', 'rgba', 'bw', 'im1', 'im8', 'im24', 'im32', 'svg', 'tga', 'vda', 'icb', 'vst', 
	# 'tif', 'tiff', 'bmp', 'xbm', 'icon', 'bitmap', 'xpm', 'xwd', 'pcx', 'pcc', 'torrent', 'mpeg', 'mp1v', 
	# 'mpg1', 'pim1', 'mp2v', 'mpg2', 'vcr2', 'hdv1', 'hdv2', 'hdv3', 'mxn', 'mxp', 'div1', 'div2', 'div3', 
	# 'mp41', 'mp42', 'mpg3', 'mpg4', 'div4', 'div5', 'div6', 'col1', 'col0', '3ivd', 'divx', 'xvid', 'mp4s', 
	# 'm4s2', 'xvid', 'mp4v', 'fmp4', '3iv2', 'smp4', 'h261', 'h262', 'h263', 'h264', 's264', 'avc1', 'davc',
	# 'x264', 'vssh', 'svq1', 'svq3', 'cvid', 'thra', 'wmv1', 'wmv2', 'wmv3', 'wvc1', 'wmva', 'vp31', 'vp30', 
	# 'vp3', 'vp50', 'vp5', 'vp51', 'vp60','vp61', 'vp62', 'vp6f', 'vp6a', 'vp7', 'fsv1', 'iv31', 'iv32', 'iv41', 
	# 'iv51', 'rv10', 'rv13', 'rv20', 'rv30', 'rv40', 'bbcd', 'rle', 'smc', 'rpza', 'qdrw', 'asv1', 'mpga', 'mp3', 
	# 'lame', 'mp4a', 'a52', 'a52b', 'ilbc', 'qclp', 'lpcj', '28_8', 'dnet', 'sipr', 'cook', 'atrc', 'raac', 'racp', 
	# 'ralf', 'shrn', 'spec', 'vorb', 'dts', 'flac', 'alac', 'samr', 'sonc', '3gp', 'asf', 'wmv', 'au', 'avi', 'flv', 
	# 'mov', 'mp4', 'ogm', 'ogg', 'mkv', 'mka', 'ts', 'mpg', 'nsc', 'nsv', 'nut', 'ra', 'ram', 'rm', 'rv', 'rmbv', 
	# 'vid', 'tta', 'tac', 'ty', 'wav', 'xa']
	itemz = ['jpg', 'mpg']
	#drop terms into queue
	for item in itemz:
		searchQueue.put(item)
	#create a bunch of queue threads
	for i in xrange(0,len(itemz)-1):
		t = Thread(target=Queues().search_worker(),name="search-%d" % (i)).start()
		t = Thread(target=Queues().download_worker(),name="download-%d" % (i)).start()
	sys.exit()

if __name__=="__main__":
	main()
