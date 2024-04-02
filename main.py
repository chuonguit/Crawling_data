from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen('https://www.uniqlo.com/vn/vi/products/E470993-000?colorCode=COL08&sizeCode=SMA003')
bs = BeautifulSoup(html.read(), 'html.parser')

namelist = bs.findAll('span', {'class':'green'})
for name in namelist:
    print(name.get_text())