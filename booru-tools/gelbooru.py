import requests, json, re, os, time, ast, random
import pixiv_tools as pixiv
from requests_html import HTMLSession
from pathlib import Path

def GetGelbooruPosts(tags = "", limit = 1):
    r = requests.get("https://gelbooru.com/index.php?page=dapi&s=post&q=index&limit=" + limit + "&tags=" + tags + "&json=1")

    return r

def GetSource(jstr):
       j = json.loads(jstr)
       source = []
       for i in j['post']:
             if i['source'] not in source:
                source.append(i['source'])

       return source
         
def main():
      r = GetGelbooruPosts(input("Tags:\n   "), input("Limit?:\n    "))
      source = GetSource(r.content)
      filename = input("FileName?:\n    ")
      Path(filename).mkdir()
      f = open(filename+"/"+filename+".txt", "w")
      f.write(json.dumps(source, indent=4))
      f.close

      for item in source:
           if(re.search(r"pixiv", item)):
                id = re.search(r"([^\/]+$)", item)
                url = pixiv.ScrapePixiv(item, id[0])
                print("return URL: ")
                print(url)
                response = requests.get(url, headers=pixiv.GetHeaders(), cookies=pixiv.GetCookies())
                with open(filename+"/"+id[0]+"."+re.search(r"[^\.]+$", url)[0], "wb") as fp:
                    fp.write(response.content)
                
                time.sleep(random.randrange(1,5))
           else:
                print(False)

main()
print("\n\nDone!")