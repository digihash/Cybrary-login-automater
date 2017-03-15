#!/usr/bin/env python

import os, time, pycurl, cStringIO, subprocess
from bs4 import BeautifulSoup

def append_log(out, file):
    with open(file, 'a+') as f:
        f.write(out)
    f.close()    

def create_curl_obj(login_url, data, ua):
    
    #set options for login
    c = pycurl.Curl()
    c.setopt(c.URL, login_url)
    #c.setopt(c.PROXY, 'https://proxy.iiit.ac.in:8080')
    c.setopt(c.POSTFIELDS, data)
    # Follow redirects
    c.setopt(c.FOLLOWLOCATION, True)
    c.setopt(c.USERAGENT, ua)
    c.setopt(c.HEADER, 1)
    #c.setopt(c.NOBODY, 1)#header only, no body
    #c.setopt(c.VERBOSE, True)
    """When we set cookiefile value to an empty string,then cURL is 
    made cookie-aware, and will catch cookies and re-send cookies
    upon subsequent requests. Hence, we can keep state between 
    requests on the same cURL handle intact."""
    c.setopt(c.COOKIEFILE, '')
    return c

def fetch_last_cyb(file):
    with open(file, 'r+') as f:
        #seek the last 28 chars of the file so you start on the last 2 lines
        f.seek(-28, os.SEEK_END)
        # Read the line and filter out the Integer value.
	totalcyb = getInteger(f.readline())
        cyb = getInteger(f.readline())
        return (totalcyb, cyb)
    f.close()    

# get the integer out of a string
def getInteger(str1):
    return int(filter(str.isdigit, str1))

def login(login_url, iurl, data, ua):
    out = "Logging In..." + "\n"

    totalcybytes = 0
    cybytes = 0
    headers = cStringIO.StringIO()
    body = cStringIO.StringIO()

    c = create_curl_obj(login_url, data, ua)
    c.setopt(c.HEADERFUNCTION, headers.write)
    
    try:
    	c.perform()
    except pycurl.error, e:
    	out += "Unexpected Error: " + str(e[0]) + " " + str(e[1]) + "\n"
    	cybytes = -1
    	return (out, cybytes)

    lstatus = c.getinfo(pycurl.HTTP_CODE)
    if lstatus != 200:
        out += "Error logging in!! Login Status: " + str(lstatus) + "\n"
        return (out, cybytes)

    #headers = cStringIO.StringIO()
    #modify options for fetching an inside url which should 
    #be accessible only after a successful authorization
    c.setopt(c.URL, iurl)
    #c.setopt(c.NOBODY, 0)
    c.setopt(c.HTTPGET, 1)
    c.setopt(c.WRITEFUNCTION, body.write)
    try:
    	c.perform()
    except pycurl.error, e:
    	out += "Unexpected Error: " + str(e[0]) + " " + str(e[1]) + "\n"
    	cybytes = -1
    	return (out, cybytes)
    		
    fstatus = c.getinfo(pycurl.HTTP_CODE)
    if(fstatus != 200):
        out += "Error logging in!! Fetch Status: " + str(fstatus) + "\n"
        return (out, fstatus, cybytes)
    soup = BeautifulSoup(body.getvalue(), 'html.parser')
    cybytes_list = soup.find_all("div", class_="cybytes")
    totalcybytes = int(cybytes_list[0].text.strip())
    cybytes = int(cybytes_list[1].text.strip())
    out += "Login Successful!!" + "\n"
    return (out, totalcybytes, cybytes)

def main():
    # e.g.: "/home/testuser/Cybrary-login-automater/"
    cybpath = "<absolute_path_of_your_folder_with_slash_at_end"
    logfile = cybpath + 'cybrary.log'
    schfile = cybpath + 'reschedule_jobs'
    last_total_cyb, last_cyb = fetch_last_cyb(logfile)
    user = "<your_username>"
    password = "<your_password>"
    login_url = 'https://www.cybrary.it/wp-login.php'
    iurl = 'https://www.cybrary.it/'
    data = 'log=' + user + '&pwd=' + password + '&wp-submit=Log+In&redirect_to=&testcookie=1'
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    
    output = "Updating cybytes on " + time.strftime("%c") + "\n"
    
    #check login
    out, totalcybytes, cybytes = login(login_url, iurl, data, ua)
    output += out
    if cybytes == 0 or cybytes == -1:
        output += "Total Cybytes: " + str(last_total_cyb) + "\n"
        output += "Cybytes: " + str(last_cyb) + "\n"
    else:
    	output += "Running Scheduler\n"
    	subprocess.call(schfile)
    	output += "Job Rescheduled\n"
	output += "Total Cybytes: " + str(totalcybytes) + "\n"
    	output += "Cybytes: " + str(cybytes) + "\n"    
    append_log(output, logfile)


if __name__ == '__main__':
    main()
