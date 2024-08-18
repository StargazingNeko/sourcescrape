import browser_cookie3, requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
    'Accept': 'image/avif,image/webp,*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.pixiv.net/',
}

def main():
    browser = input("What browser do you wish to grab cookies from? Chrome or FireFox?:\n   ")
    if browser.capitalize == "CHROME":
        cookiejar = browser_cookie3.chrome(domain_name='pixiv.net')
    elif browser.capitalize == "FIREFOX":
        cookiejar = browser_cookie3.firefox(domain_name='pixiv.net')
    s = requests.Session()
    r = s.get("https://www.pixiv.net/en/artworks/24079612", cookies=cookiejar, headers=headers)

    print(r.cookies.get_dict())

    if(r.status_code == 200):
        cookies = r.cookies.get_dict()
        f = open("pixiv_cookies", "w")
        print(str(cookies))
        f.write(str(cookies))
        f.close
    else:
        print("Status was not successful")

main()