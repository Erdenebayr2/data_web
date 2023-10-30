from datetime import date, datetime, timedelta
import aiohttp,asyncio,json
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta

async def fetch_page(page_number, session):
    mlink = f'https://www.unegui.mn/l-hdlh/l-hdlh-zarna/hashaa-bajshin-ger/?page={page_number}'
    async with session.get(mlink) as response:
        content = await response.text()
        soup = BeautifulSoup(content, 'html.parser')
        links = soup.find_all('a', class_="advert__content-title")
        link_urls = [f"https://www.unegui.mn{link.get('href')}" for link in links]
        return link_urls

async def main_links(session):
    mlink = 'https://www.unegui.mn/l-hdlh/l-hdlh-zarna/hashaa-bajshin-ger/?page='
    async with session.get(mlink) as response:
        content = await response.text()
        soup = BeautifulSoup(content, 'html.parser')
        page_numbers = soup.find_all('a', class_="page-number js-page-filter")
        number = int(page_numbers[-1].text.strip())

        tasks = [fetch_page(page, session) for page in range(1, number + 1)]
        page_links = await asyncio.gather(*tasks)
        page_links = list(set(link for sublist in page_links for link in sublist))
        return page_links

async def process_page(page_url, session, data):
    async with session.get(page_url) as response:
        content = await response.text()
        soup = BeautifulSoup(content, 'html.parser')

        mark = soup.find('ul',class_='breadcrumbs').text.split('\n')
        mark = list(filter(lambda x:x.strip() != '',mark))
        manufacturer = mark[-2]
        mark = mark[-1]

        desc = soup.find('div',class_='js-description').text.split('\n')
        desc = list(filter(lambda x: x.strip() != '', desc))
        desc = ''.join(desc)

        ogno = soup.find('span', class_='date-meta').text[11:-6]
        unuudr = 'Өнөөдөр'
        uchigdur = 'Өчигдөр'
        yester = datetime.now() - timedelta(days=1)
        yesterday = str(yester.date())
        today = str(date.today())
        if ogno == unuudr:
            ogno = today
        elif ogno == uchigdur:
            ogno = yesterday
        else:
            ogno

        zar_num = soup.find('span', {'itemprop': 'sku'}).text.split('\n')
        price = soup.find('meta', {'itemprop': 'price'})['content']

        mindata = soup.find('ul', class_='chars-column').text.split('\n')
        mindata = list(filter(lambda x: x.strip() != '', mindata))
        # if len(mindata) == 32:
        #     mindata = mindata
        # elif len(mindata) == 30:
        #     if 'Урьдчилсан төлбөрийн хэмжээ:' in mindata:
        #         mindata[22:22] = ('Хаяг байршил:','')
        #     else:
        #         mindata[0:0] = ('Урьдчилсан төлбөрийн хэмжээ:','')
        # elif len(mindata) == 28:
        #     mindata[0:0] = ('Урьдчилсан төлбөрийн хэмжээ:','')
        #     mindata[22:22] = ('Хаяг байршил:','')

        dict = {}
        for i in range(0,len(mindata), 2):
            key = mindata[i].strip(':')
            value = mindata[i+1]
            dict[key] = value

        new_keys = ['Square', ' Possibility_of_leasing']
        
        new_dict = {new_key: dict[old_key] for old_key, new_key in zip(dict.keys(), new_keys)}

        data[zar_num[0]] = {'Maintype': manufacturer ,'Type': mark, 'date': ogno, 'price': price,**new_dict,'Description':desc}

async def getdata(session, data):
    all_links = await main_links(session)
    tasks = [process_page(link, session, data) for link in all_links]
    await asyncio.gather(*tasks)

async def main():
    data = {}
    timeout = aiohttp.ClientTimeout(total=300)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            await getdata(session, data)
        except asyncio.TimeoutError as e:
            print(f"Timeout error: {e}")

        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4)

if __name__ == '__main__':
    asyncio.run(main())
