import urllib.parse, urllib.request, re

async def yourl(url):
    is_url = False
    youtube_urls = ["www.youtube.com","m.youtube.com","youtu.be"]

    if (url[0:7] == "http://") or (url[0:8] == "https://"):
        is_url = True
    else:
        is_url = False

    if is_url == True:
        if any(x in url for x in youtube_urls):
            return url
        else:
            return "invalid"
    else:
        youtube_base_url = 'https://www.youtube.com/'
        youtube_results_url = youtube_base_url + 'results?'
        youtube_watch_url = youtube_base_url + 'watch?v='

        query_string = urllib.parse.urlencode({
            'search_query': url
        })

        content = urllib.request.urlopen(
            youtube_results_url + query_string
        )

        search_results = re.findall(r'/watch\?v=(.{11})', content.read().decode())

        link = youtube_watch_url + search_results[0]
        return link

async def clean_url(url):
    out = ""
    if ("www.youtube.com" in url) or ("m.youtube.com" in url):
        for char in url:
            if char == "&":
                return out
            out += char
        return out
    else:
        for char in url:
            if char == "?":
                return out
            out += char
        return out

if __name__ == "__main__":
    txts = ["https://www.youtube.com/watch?v=e-LpgXW20MM&list=RDe-LpgXW20MM","https://youtu.be/4yMX84KyfKM?si=KDsN3AtO1xmroNWY","https://bruh.com","nope","linkin park numb"]
    for i in txts:
        print(clean_url(yourl(i)))
