import xmlschema
import requests
from xml.etree import ElementTree as ET

''' Проверить API получения котировок валют по курсу ЦБ РФ.
Нужно проверить:
1. XML валидный
2. формат соответствует заявленному. есть все поля, описаннные в документе.
3. значения. что числа - это числа. что коды валют реальны.
4. любые другие проверки, которые улучшат качество сервиса и будут его контролировать в дальнейшем '''

url = "http://www.cbr.ru/scripts/XML_daily.asp"

xsd = xmlschema.XMLSchema('http://www.cbr.ru/StaticHtml/File/92172/ValCurs.xsd')

daily_val = requests.get(url).text
test = xmlschema.is_valid(daily_val, xsd)
# print(test)

# Проверка Value на число
response = requests.get(url)
tree = ET.fromstring(response.content)
for value in tree.iter("Value"):
    float(value.text.replace(",", "."))

# Проверка кодировок валют
code_list = requests.get("http://www.cbr.ru/scripts/XML_valFull.asp")
code_list = ET.fromstring(code_list.text)
print(tree.find("Valute[@ID='R01010']/NumCode").text)
for item in code_list.iter("Item"):
    item_id = item.find('./ParentCode').text.strip()
    if item_id in 'R01720' and item.attrib == {'ID': 'R01720A'}:
        continue
    tree_num_code = tree.find(f"Valute[@ID='{item_id}']/NumCode")
    tree_char_code = tree.find(f"Valute[@ID='{item_id}']/CharCode")
    list_num_code = item.find("./ISO_Num_Code")
    list_char_code = item.find("./ISO_Char_Code")
    if tree_num_code is not None:
        print(int(tree_num_code.text))
        print(int(list_num_code.text))
        print(tree_char_code.text)
        print(list_char_code.text)
        print(int(tree_num_code.text) == int(list_num_code.text))
        print(tree_char_code.text == list_char_code.text)

# print(item.find("NumCode").text)
# print(item.find("CharCode").text)
# print(tree.find(f"Valute[@ID='{item_id}']/NumCode").text)
