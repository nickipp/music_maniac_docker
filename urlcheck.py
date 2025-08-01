import urllib.parse, urllib.request, re

async def yourl(url):
    youtube_urls = ["www.youtube.com","m.youtube.com","youtu.be"]

    if (url[0:7] == "http://") or (url[0:8] == "https://"):
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

        content = await urllib.request.urlopen(
            youtube_results_url + query_string
        )

        search_results = re.findall(r'/watch\?v=(.{11})', content.read().decode())

        link = youtube_watch_url + search_results[0]

        return link

def clean_url(url):
    out = ""
    if ("www.youtube.com" in url) or ("m.youtube.com" in url):
        for char in url:
            if char == "&":
                return out
            out += char
    else:
        for char in url:
            if char == "?":
                return out
            out += char
    return out