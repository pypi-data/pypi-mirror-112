
import requests
# data="";
# r=requests.post("http://139.196.146.45:8881/search/pos-result",data,{"JobTypeName":"电工"});
# print(r.text)
# print(r.content)
from bs4 import BeautifulSoup
##
## @description get link
##
def GetMovieLink(url):
     r=requests.get(url);
     htmltxt=r.content
     soup=BeautifulSoup(htmltxt,'html.parser')
     alla=soup.find_all('input', attrs={"type":"checkbox","class":"down_url"});
     movielinks=[]
     for link in alla:
          linkstr=link.get('value')
          if(linkstr!=None):
               movielinks.append(linkstr)
     return movielinks
