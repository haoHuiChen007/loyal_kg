import requests
from lxml import etree

for page in range(1):
    url = "https://china.findlaw.cn/ask/wenda/browse_page"+str(page)
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42",
    }
    html = requests.get(url)
    tree = etree.XML(html)
    result = tree.xpath("/html/body/div[3]/div[2]/div[1]/div[2]/ul/text()")
    print(result)
    # /html/body/div[3]/div[2]/div[1]/div[2]/ul
    # car_list = resp['data']['series']
    # car_img_urls = []
    # for car_img_url in car_list:
    #     car_img_url = car_img_url['cover_url']
    #     img_file_name = car_img_url.split('/')[-1]
    #     img = requests.get(car_img_url, headers=header)
    #     img_file_name = str(img_file_name)[0:15] + '.png'
    #     print(img_file_name)
    #     with open("./images/" + str(img_file_name).rstrip(':'), "wb") as f:
    #         f.write(img.content)