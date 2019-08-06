import requests, os, re, wget, pprint
from bs4 import BeautifulSoup as soup

def auth():
    site = 'https://yandex.ru'

    session.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'
    resp = session.get(site)

    print(f'\nStatus code for {site} is: {resp.status_code}\n')
    print('Headers: \n')

    for key, val in resp.headers.items():
        print(f'{key}: {val}')

with requests.Session() as session:
    auth()

# Ответ:
#
# Status code for https://yandex.ru is: 200
#
# Headers:
#
# Date: Tue, 06 Aug 2019 10:51:47 GMT
# Content-Type: text/html; charset=UTF-8
# Cache-Control: no-cache,no-store,max-age=0,must-revalidate
# Expires: Tue, 06 Aug 2019 10:51:47 GMT
# Last-Modified: Tue, 06 Aug 2019 10:51:47 GMT
# Content-Security-Policy: connect-src 'self' wss://webasr.yandex.net https://mc.webvisor.com https://mc.webvisor.org wss://push.yandex.ru wss://portal-xiva.yandex.net https://yastatic.net https://home.yastatic.net https://yandex.ru https://*.yandex.ru static.yandex.sx brotli.yastatic.net et.yastatic.net *.serving-sys.com an.yandex.ru awaps.yandex.ru storage.mds.yandex.net music.yandex.ru music-browser.music.yandex.net mc.admetrica.ru msk-cdn-exp.yastatic.net msk-cdn-etl.yastatic.net yastat.net br.yastatic.net portal-xiva.yandex.net yastatic.net home.yastatic.net yandex.ru *.yandex.ru *.yandex.net yandex.st; default-src 'self' blob: wss://portal-xiva.yandex.net yastatic.net yastat.net portal-xiva.yandex.net; font-src 'self' https://yastatic.net zen.yandex.ru static.yandex.sx brotli.yastatic.net et.yastatic.net yabro1.zen-test.yandex.ru main.zdevx.yandex.ru msk-cdn-exp.yastatic.net msk-cdn-etl.yastatic.net yastat.net br.yastatic.net yastatic.net; frame-src 'self' yabrowser: data: https://ott-widget.yandex.ru https://www.youtube.com https://player.video.yandex.net https://ya.ru https://ok.ru https://yastatic.net https://yandex.ru https://*.yandex.ru https://downloader.yandex.net wfarm.yandex.net secure-ds.serving-sys.com yandexadexchange.net *.yandexadexchange.net music.yandex.ru music.yandex.kz yastatic.net yandex.ru *.yandex.ru awaps.yandex.net *.cdn.yandex.net; img-src 'self' data: https://leonardo.edadeal.io https://yastatic.net https://home.yastatic.net https://*.yandex.ru https://*.yandex.net https://*.tns-counter.ru awaps.yandex.net *.yastatic.net gdeua.hit.gemius.pl pa.tns-ua.com mc.yandex.com mc.webvisor.com mc.webvisor.org static.yandex.sx brotli.yastatic.net et.yastatic.net *.moatads.com avatars.mds.yandex.net bs.serving-sys.com an.yandex.ru awaps.yandex.ru nissanhelioseurope.demdex.net mc.admetrica.ru msk-cdn-exp.yastatic.net msk-cdn-etl.yastatic.net yastat.net br.yastatic.net *.yandex.net resize.yandex.net yastatic.net home.yastatic.net yandex.ru *.yandex.ru *.tns-counter.ru yandex.st; media-src 'self' blob: data: *.storage.yandex.net *.yandex.net strm.yandex.ru strm.yandex.net *.strm.yandex.net *.cdn.yandex.net storage.mds.yandex.net *.storage.mds.yandex.net yastatic.net kiks.yandex.ru; object-src 'self' *.yandex.net music.yandex.ru strm.yandex.ru flashservice.adobe.com yastatic.net kiks.yandex.ru awaps.yandex.net storage.mds.yandex.net; report-uri https://csp.yandex.net/csp?project=morda&from=morda.big.ru&showid=1565088707.07808.122104.156367&h=sas1-0686-sas-portal-morda-17154&csp=old&date=20190806&yandexuid=9877934731565088707; script-src 'self' 'unsafe-inline' 'unsafe-eval' blob: https://suburban-widget.rasp.yandex.ru https://suburban-widget.rasp.yandex.net https://music.yandex.ru https://mc.yandex.fr https://mc.webvisor.com https://yandex.fr https://mc.webvisor.org https://yastatic.net https://home.yastatic.net https://mc.yandex.ru https://pass.yandex.ru zen.yandex.ru an.yandex.ru api-maps.yandex.ru static.yandex.sx webasr.yandex.net brotli.yastatic.net et.yastatic.net z.moatads.com bs.serving-sys.com secure-ds.serving-sys.com yabro1.zen-test.yandex.ru main.zdevx.yandex.ru awaps.yandex.ru storage.mds.yandex.net msk-cdn-exp.yastatic.net msk-cdn-etl.yastatic.net yastat.net br.yastatic.net yastatic.net home.yastatic.net yandex.ru www.yandex.ru mc.yandex.ru suggest.yandex.ru clck.yandex.ru awaps.yandex.net; style-src 'self' 'unsafe-inline' https://yastatic.net https://home.yastatic.net zen.yandex.ru static.yandex.sx brotli.yastatic.net et.yastatic.net yabro1.zen-test.yandex.ru main.zdevx.yandex.ru msk-cdn-exp.yastatic.net msk-cdn-etl.yastatic.net yastat.net br.yastatic.net yastatic.net home.yastatic.net;
# P3P: policyref="/w3c/p3p.xml", CP="NON DSP ADM DEV PSD IVDo OUR IND STP PHY PRE NAV UNI"
# Set-Cookie: yp=1567680707.ygu.1; Expires=Fri, 03-Aug-2029 10:51:47 GMT; Domain=.yandex.ru; Path=/, mda=0; Expires=Wed, 04-Dec-2019 10:51:47 GMT; Domain=.yandex.ru; Path=/, yandex_gid=213; Expires=Thu, 05-Sep-2019 10:51:47 GMT; Domain=.yandex.ru; Path=/, yandexuid=9877934731565088707; Expires=Fri, 03-Aug-2029 10:51:47 GMT; Domain=.yandex.ru; Path=/, i=ye0YzSXEyi7KEBk4OQzk4I+jl3vFdc5kNC7hdXN6kKfetzEyYD/iv3Y5CjsaFCPE/QH3PkqFLNl6suMI9MYNjBXXaFk=; Expires=Fri, 03-Aug-2029 10:51:47 GMT; Domain=.yandex.ru; Path=/; Secure; HttpOnly
# X-Frame-Options: DENY
# X-Yandex-STS: 1
# Content-Encoding: gzip
# X-Content-Type-Options: nosniff
# Transfer-Encoding: chunked