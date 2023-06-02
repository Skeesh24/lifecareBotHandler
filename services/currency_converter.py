from requests import get
from xml.etree.cElementTree import ElementTree, parse
from datetime import datetime
from os.path import exists


def downloadContent(path: str) -> None:
    lines = get(
        f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={datetime.now().strftime('%d/%m')}/20{datetime.now().strftime('%y')}").content.decode("windows-1251")

    lines = lines.replace("windows-1251", "utf-8")

    with open(path, "w", encoding="windows-1251") as file:
        file.write(lines)


def parseXML(path: str) -> ElementTree:
    lines = "".join(open(path).readlines())
    try:
        index = lines.replace("Date=\"", "*").index("*")
    except:
        downloadContent(path)

    day_month_xml = lines[index+6:index+11]

    if not exists(path) or datetime.now().date().strftime("%d.%m") != day_month_xml:
        downloadContent(path)

    with open(path) as xml:
        return parse(xml)


def getCurrencyValute(path: str, valute_charcode: str) -> int:
    flag = False
    iter = 0

    try:
        for valutes in parseXML(path).getroot():
            for valute in valutes:
                if flag:
                    iter += 1
                if valute.text == valute_charcode:
                    flag = True
                if iter == 3:
                    return int(valute.text.replace(",", "."))
    except Exception as e:
        print(e)


# return usd
def rub_to_usd(rubs: float) -> int:
    return round(getCurrencyValute("services/content.xml", "USD") / rubs)


# return eur
def rub_to_eur(rubs: float) -> int:
    return round(getCurrencyValute("services/content.xml", "EUR") / rubs)


# return rub
def usd_to_rub(usds: float) -> int:
    return round(getCurrencyValute("services/content.xml", "USD") * usds)


# return rub
def eur_to_rub(eurs: float) -> int:
    return round(getCurrencyValute("services/content.xml", "EUR") * eurs)
