Scraper tool for Gelbooru, this tool will prioritize the *source* linked in the post. If supported and the source still exists, it will attempt to download the original quality image/video from the source otherwise it will download original from Gelbooru.

Tool is being designed in a modular way so if you so chose to, you can also directly download from the supported sites.

# How to use this tool?
> (Note: Currently there is only a shell script for Linux, Windows isn't currently supported but it should still work on Windows since it's Python, you'll just have to write your own batch script. Windows will be done officially in the near future)

1. >./scrape.sh gelbooru \<tags></blockquote>
examples:
<br>`./scrape gelbooru tokoyami_towa`
<br>`./scrape gelbooru tokoyami_towa+rating:general`

    **OR**
2. >./scrape \<supported_site> \<link></blockquote>
example:
<br>`./scrape pixiv https://www.pixiv.net/en/artworks/122755230`