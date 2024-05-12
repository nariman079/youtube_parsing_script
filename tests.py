"""
-- Test download file by parts --
"""
import requests

def download_file(url: str) -> None:
    """ Download file """
    r = requests.get(url, timeout=40)
    # f = open('local_filename.mp4', 'wb')
    print(r.content)
    # for chunk in  tqdm.tqdm(r.iter_content(chunk_size=512),total=10):
    #     if chunk:
    #         f.write(chunk)
    # f.close()

url = r"""

https://rr1---sn-xaxjugvn8t51-hjm6.googlevideo.com/videoplayback?expire=1715560137&ei=aQpBZrL1Ovml0u8PxpyikAM&ip=195.19.125.173&id=o-AMiF2HWe8lpXz7M3_eZnjDdB3PJehpdncoV1vJR3aFAI&itag=313&aitags=133%2C134%2C135%2C136%2C137%2C160%2C242%2C243%2C244%2C247%2C248%2C271%2C278%2C313&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&mh=Nb&mm=31%2C29&mn=sn-xaxjugvn8t51-hjm6%2Csn-n8v7znly&ms=au%2Crdu&mv=m&mvi=1&pl=24&initcwndbps=1645000&bui=AWRWj2R1egnFt9CpMF6EO1XASojddtRGZzoatl2dM5CAA9d0wzcZqxNPTGh-WjvuyG-XniYq9D11gCyD&spc=UWF9fwHcvSaX4Qqh7CW9HgyaFbFOspc4tGVismGq0uYk95Y&vprv=1&svpuc=1&mime=video%2Fwebm&ns=BnDGMm8hYBx7xvqXyHTdP6AQ&rqh=1&gir=yes&clen=54780455&dur=58.680&lmt=1714287974308443&mt=1715538049&fvip=11&keepalive=yes&c=WEB_EMBEDDED_PLAYER&sefc=1&txp=630A224&n=L5Y8QKJECKcLZqYO4&sparams=expire%2Cei%2Cip%2Cid%2Caitags%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Cns%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AJfQdSswRAIgKP3DlZsIxWdabOLYH8bJqR3MSmkj0CcbDEQ1VvUiYWMCIFbIWx03OFrSM8nKRr63u-lUyHFuprvtFRM78qZiru7G&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AHWaYeowRgIhAN24YAKEJ6bkPcX7hYli8LTevwx_rjqHsnMXwwWuX7xEAiEAs11M3bNpkyMIcpEhOm_SpNPpFIw-5FmgH7aweKiQV6g%3D

"""
download_file(url=url)