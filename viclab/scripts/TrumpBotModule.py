#!/usr/bin/python

import re,os,time,datetime,subprocess,sys
import os.path
import platform
from shutil import copyfile


class DateString:

  def __init__(self):
    self.yesterday = str(datetime.date.fromtimestamp(time.time() - (60*60*24) ).strftime("%Y-%m-%d"))
    self.today = str(datetime.date.fromtimestamp(time.time()).strftime("%Y-%m-%d"))
    self.tomorrow = str(datetime.date.fromtimestamp(time.time() + (60*60*24) ).strftime("%Y-%m-%d"))
    self.now = str(time.strftime('%X %x %Z'))


class SQLTools:

  def MakeTables(self,cur):
    # Make some fresh tables using executescript()
    cur.executescript('''
  
    DROP TABLE IF EXISTS TRUMPBS;
   

    CREATE TABLE TRUMPBS (
      id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
      bullshit    BLOB,
      category    TEXT
    );



    ''')

class Files:

  def __init__(self):
    self.dir = ''
    self.data = []
    self.file_exists = 0

  def mkdir(self):
    if not os.path.isdir(self.dir):
      if 'Win' in platform.system():
        subprocess.call(["md", self.dir], shell=True)
      else:
        subprocess.call(["mkdir", self.dir])

  def write_file(self,filename,list):
    f = open(filename,'w')
    for line in list:
      f.write(line + '\n')
    f.close()

  def write_file_append(self,filename,list):
    f = open(filename,'a')
    for line in list:
      f.write(line)
    f.close()

  def write_log(self,logfile,logentry):
    f = open(logfile,'a')
    reportDate =  str(time.strftime("%x - %X"))
    f.write(reportDate + " :" + logentry)
    f.close()

  def read_file(self,filename):
    self.data = []
    self.file_exists = 1
    # Testing if file exists.
    if os.path.isfile(filename):
      try:
        f = open(filename,'r')
      except IOError:
        print "Failed opening ", filename
        sys.exit(2)
      for line in f:
        line = line.strip()
        self.data.append(line)
      f.close()
    else:
      # Set the file_exists flag in case caller cares.
      self.file_exists = 0

  def copy_file(self,src, dest):
    try:
      copyfile(src, dest)
    except IOError:
      print "Failed file copy ", src,dest
      sys.exit(2)

    
  def stat_file(self,fname):
    blocksize = 4096
    hash_sha = hashlib.sha256()
    f = open(fname, "rb")
    buf = f.read(blocksize)
    while 1:
      hash_sha.update(buf)
      buf = f.read(blocksize)
      if not buf:
        break    
    checksum =  hash_sha.hexdigest()
    filestat = os.stat(fname)
    filesize = filestat[6]
    return checksum,filesize

class HTML5:

  def __init__(self):
    self.tr = '<tr>'
    self.td = '<td>'
    self.th = '<th>'
    self.end_table = '\n</table>\n'
    self.end_html = '  </body>\n</html>\n'
    self.http_header = 'Content Type: text/html\n\n'
    self.stylesheet = '''
<style>
#header {
    background-color:black;
    color:white;
    text-align:center;
    padding:5px;
}
#nav {
    line-height:30px;
    height:400px;
    width:15%;
    float:left;
    padding:5px;
    overflow:auto;
    background-color:#eeeeee;    
}
#section {
    width:80%;
    float:left;
    padding:10px;
}
#footer {
    background-color:black;
    color:white;
    clear:both;
    text-align:center;
    padding:5px;
}
#nav_content
{
  overflow:auto;
  background:#fff;
}
#section_content
{
  height:655px;
  overflow:auto;
  background:#fff;
  padding:10px;
}
p.small 
{
    line-height: 30px;
}
p.big 
{
    line-height: 60px;
}
td {
  text-align: right;
}
th {
  text-align: center;
}
h1 {
  color: blue;
}

h3 
   { 
     color: blue; 
     background-color: ; 
     margin-top: 0px;
     margin-bottom: 0px;
   }
h3:hover 
   { 
     color: white; 
     background-color: blue; 
     transition: all 250ms ease-in-out; 
   }    

h4 
   { 
     color: blue; 
     background-color: ; 
     margin-top: 0px;
     margin-bottom: 0px;
   }
h4:hover 
   { 
     color: white; 
     background-color: blue; 
     transition: all 250ms ease-in-out; 
   }    

</style>'''    
    
    



  def style_sheet(self,cssfile='reportstyle.css'):


    f = open('Report/css/' + cssfile,'w')
    f.write(self.stylesheet)
    f.close()
   
    
 
  
  def th_list(self,row,bgcolor='#BAB9B8'):
    
    html = '      <tr bgcolor=' + bgcolor + '>'
    for cell in row:
      html += '<th>' + str(cell) + '</th>'
    html += '</tr>\n'
    return html

  def tr_list(self,row,attr=False):
    

    html = '      <tr>'
    for cell in row:
      if attr:
        html += '<td ' + attr + '>' + str(cell) + '</td>'
      else:
        html += '<td>' + str(cell) + '</td>'
    html += '</tr>\n'
    return html   
 
 
  def start_html(self,title='Web Report Page',align='center'): 
    html =   '<!DOCTYPE html>\n<html>\n'
    html +=  '  <head><title>' + title + '</title>\n'
    html +=  '  <meta charset="UTF-8">\n'
    html +=  '  <link href="../css/reportstyle.css" rel="stylesheet" />\n'
    html +=  '  <link href="css/reportstyle.css" rel="stylesheet" />\n'
    #html +=  self.stylesheet
    html +=  '  </head>\n'
    html +=  '  <body align="' + align + '">\n'
    return  html
    
       

  def start_table(self,align='center',border='1',caption='',width='100%'):
    html =  '\n\n'
    #html += '<p><br>\n'
    html += '<table align="' + align +  '" border="' + str(border)
    html += '" width="' + width + '">\n'
    if caption != '':
      html += '<caption>' + caption + '</caption>\n'
    return  html
 

  def insert_table(self,rows,headings,align='center',border='1',caption=''):
    html =  '\n\n'
    html += '<p><br>\n'
    html += '<table align="' + align +  '" border="' + str(border) + '">\n'
    html += '<caption>' + caption + '</caption>\n'
    for row in rows:
      html += self.tr_list(row)
    html += self.end_table
    return  html


  def header(self,content):
    code = '<div id="header"><br>\n'
    code += content + '\n</div>\n'
    return code

  def nav(self,content):
    code = '<div id="nav">\n'
    code += content + '\n</div>\n'
    return code

  def section(self,content):
    code = '<div id="section">\n'
    code += content + '\n</div>\n'
    return code

  def footer(self,content):
    code = '<div id="footer">\n'
    code += content + '\n</div>\n'
    return code







