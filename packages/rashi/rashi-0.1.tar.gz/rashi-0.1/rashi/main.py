import enum
import requests
from typing import NamedTuple
from bs4 import BeautifulSoup as bs


class Rashi(NamedTuple):
    rashi: str
    date: str


class Zodiacs(enum.Enum):
    Mesh = 'Mesh'
    Mithun = 'Mithun'
    Singha = 'Singha'
    Tula = 'Tula'
    Dhanu = 'Dhanu'
    Kumbha = 'Kumbha'
    Brish = 'Brish'
    Karkat = 'Karkat'
    Kanya = 'Kanya'
    Brischik = 'Brischik'
    Makar = 'Makar'
    Meen = 'Meen'


class Length(enum.Enum):
    Daily = 'daily'
    Weekly = 'weekly'
    Monthly = 'monthly'
    Yearly = 'yearly'


def getRashiFal(zodiac: Zodiacs, length: Length) -> Rashi:
    baseURL = f"https://www.hamropatro.com/rashifal/{length.value}/{zodiac.value}"
    print(baseURL)
    response = requests.get(baseURL).content
    soup = bs(response, "html.parser")
    rashi: str = soup.find_all("p")[0].text.split("- ज्य")[0]
    rashiDate: str = soup.select(
        "#content > div > div:nth-child(1) > div.container12 > div.column7 > h2 > span > a")[0].text
    return Rashi(rashi, rashiDate)


if __name__ == "__main__":
    rashi = getRashiFal(Zodiacs.Meen, Length.Weekly)
    print(rashi.rashi)
    print(rashi.date)
