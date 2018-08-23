from bs4 import BeautifulSoup

import requests

# �� ���� ��ȭ�� ���� ������ ��� ��ü�Դϴ�.
class Conversation:
    
    # ����(Question), ����(Answer) �� ������ �����˴ϴ�.
    def __init__(self, contentName, contentType, question, answer):
        self.contentName = contentName
        self.contentType = contentType
        self.question = question
        self.answer = answer

    def __str__(self):
        return "����: " + self.question + "\n�亯: " + self.answer + "\n"

# ��� ���� ��ȭ ������ �����ϴ� �Լ��Դϴ�.
def get_subjects():
    subjects = []

    # ��ü ���� ����� �����ִ� ���������� ��û(Request) ��ü�� �����մϴ�.
    req  = requests.get('https://basicenglishspeaking.com/daily-english-conversation-topics/')
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.findAll('div',{"class": "su-column-inner"})

    for div in divs:
        # ���ο� �����ϴ� <a> �±׵��� �����մϴ�.
        links = div.findAll('a')

        # <a> �±� ������ �ؽ�Ʈ�� ����Ʈ�� �����մϴ�.
        for link in links:
            subject = link.text
            subjects.append(subject)
    return subjects

subjects = get_subjects()

print('�� ', len(subjects), '���� Ÿ���� ã�ҽ��ϴ�.')

print(subjects)

conversations = []
i = 1
count = 1

# ��� ��ȭ ���� ������ �����մϴ�.
for sub in subjects:
    print('(', i, '/', len(subjects), ') ', sub, ': ', len(conversations), "��")
    # ��ȭ ��ũ��Ʈ�� �����ִ� ���������� ��û(Request) ��ü�� �����մϴ�.
    req  = requests.get('http://basicenglishspeaking.com/' + sub.replace(" ", "-"))
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    qnas = soup.findAll('div',{"class": "sc_player_container1"})

    # ������ ��ȭ ���뿡 ��� �����մϴ�.
    for qna in qnas:
        if qnas.index(qna) % 2 == 0:
            q = qna.next_sibling
        else:
            a = qna.next_sibling
            c = Conversation(sub, count, q, a)
            conversations.append(c)
            count = count + 1
    i = i + 1

print('�� ', len(conversations), '���� ��ȭ�� ã�ҽ��ϴ�.')

# ��� ��ȭ ������ ����մϴ�.
for c in conversations:
    print(str(c))

# �ڵ�ȭ �׽�Ʈ�� ���� �����Ͽ�(Selenium)�� �ҷ��ɴϴ�.
from selenium import webdriver

# ũ�� �� ����̹��� ��θ� �����մϴ�.
driver = webdriver.Chrome('C:\Chrome Driver\Chrome Driver.exe')

# ũ���� ���� Paraphrase ���� ����Ʈ�� �����մϴ�.
driver.get('https://articlerewritertool.com/')

dic = {}
# conversations Length�� �þ�� ���� �ذ� �ʿ�
for i in range(0, len(conversations)):
    c = conversations[i]
    question = c.question
    dic[question] = True
    print("<", i, " - [", c.contentType, "] > ", str(c))
    
    driver.find_element_by_name('formNameLabelTextBefore').clear()
    driver.find_element_by_name('formNameLabelTextBefore').send_keys(question)
    driver.execute_script("document.getElementsByName('math_captcha_equation')[0].setAttribute('value', 'two minus one')")
    driver.find_element_by_name('math_captcha_answer').clear()
    driver.find_element_by_name('math_captcha_answer').send_keys('1')

    driver.find_element_by_xpath('/html/body/center/section/form/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td[2]/p[2]/input').click()

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    if soup.find("textarea", {"name":"formNameLabelTextAfter"}) is None:
        print('None Result Found')
        i = i - 1
        driver.get('https://articlerewritertool.com/')
        continue;
    result = soup.find("textarea", {"name":"formNameLabelTextAfter"}).text

    if result not in dic:
        temp = Conversation(c.contentName, c.contentType, c.question, c.answer)
        temp.question = result
        dic[result] = True
        conversations.insert(i + 1, temp)

# ��� ��ȭ ������ ����մϴ�.
for c in conversations:
    print(str(c))
    
print('�� ', len(conversations), '���� ��ȭ�� �����մϴ�.')

import xlsxwriter

# ���� ��ũ �� �� ��ũ ��Ʈ�� �����մϴ�.
workbook = xlsxwriter.Workbook('Conversation Data.xlsx')
worksheet = workbook.add_worksheet()

row = 0
col = 0

# ��� ��ȭ ������ ������ �����մϴ�.
for c in conversations:
    worksheet.write(row, col, c.contentName)
    worksheet.write(row, col + 1, c.contentType)
    worksheet.write(row, col + 2, c.question)
    worksheet.write(row, col + 3, c.answer)
    row = row + 1
    
workbook.close()

# -*- coding: utf-8 -*-

# Dialog Flow�� Import�� �� �ִ� Intent ���Ϸ� ����ϱ�
i = 1
# ���, �Է� �� JSON ������ �����մϴ�.
prev = str(conversations[0].contentName) + str(conversations[0].contentType)
f = open(prev + '.json', 'w', encoding='UTF-8')
f.write('{ "id": "10d3155d-4468-4118-8f5d-15009af446d0", "name": "' + prev + '", "auto": true, "contexts": [], "responses": [ { "resetContexts": false, "affectedContexts": [], "parameters": [], "messages": [ { "type": 0, "lang": "ko", "speech": "' + conversations[0].answer + '" } ], "defaultResponsePlatforms": {}, "speech": [] } ], "priority": 500000, "webhookUsed": false, "webhookForSlotFilling": false, "fallbackIntent": false, "events": [] }')
f.close()
f = open(prev + '_usersays_ko.json', 'w', encoding='UTF-8')
f.write("[")
f.write('{ "id": "3330d5a3-f38e-48fd-a3e6-000000000001", "data": [ { "text": "' + conversations[0].question + '", "userDefined": false } ], "isTemplate": false, "count": 0 },')

while True:
    if i >= len(conversations):
        f.write("]")
        f.close()
        break;
    c = conversations[i]
    if prev == str(c.contentName) + str(c.contentType):
        f.write('{ "id": "3330d5a3-f38e-48fd-a3e6-000000000001", "data": [ { "text": "' + c.question + '", "userDefined": false } ], "isTemplate": false, "count": 0 },')
    else:
        f.write("]")
        f.close()
        # ���, �Է� �� JSON ������ �����մϴ�.
        prev = str(c.contentName) + str(c.contentType)
        f = open(prev + '.json', 'w', encoding='UTF-8')
        f.write('{ "id": "10d3155d-4468-4118-8f5d-15009af446d0", "name": "' + prev + '", "auto": true, "contexts": [], "responses": [ { "resetContexts": false, "affectedContexts": [], "parameters": [], "messages": [ { "type": 0, "lang": "ko", "speech": "' + c.answer + '" } ], "defaultResponsePlatforms": {}, "speech": [] } ], "priority": 500000, "webhookUsed": false, "webhookForSlotFilling": false, "fallbackIntent": false, "events": [] }')
        f.close()
        f = open(prev + '_usersays_ko.json', 'w', encoding='UTF-8')
        f.write("[")
        f.write('{ "id": "3330d5a3-f38e-48fd-a3e6-000000000001", "data": [ { "text": "' + c.question + '", "userDefined": false } ], "isTemplate": false, "count": 0 },')
    i = i + 1