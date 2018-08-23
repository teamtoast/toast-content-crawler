from bs4 import BeautifulSoup

import requests

# 한 건의 대화에 대한 정보를 담는 객체입니다.
class Conversation:
    
    # 질문(Question), 응답(Answer) 두 변수로 구성됩니다.
    def __init__(self, contentName, contentType, question, answer):
        self.contentName = contentName
        self.contentType = contentType
        self.question = question
        self.answer = answer

    def __str__(self):
        return "질문: " + self.question + "\n답변: " + self.answer + "\n"

# 모든 영어 대화 주제를 추출하는 함수입니다.
def get_subjects():
    subjects = []

    # 전체 주제 목록을 보여주는 페이지로의 요청(Request) 객체를 생성합니다.
    req  = requests.get('https://basicenglishspeaking.com/daily-english-conversation-topics/')
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.findAll('div',{"class": "su-column-inner"})

    for div in divs:
        # 내부에 존재하는 <a> 태그들을 추출합니다.
        links = div.findAll('a')

        # <a> 태그 내부의 텍스트를 리스트에 삽입합니다.
        for link in links:
            subject = link.text
            subjects.append(subject)
    return subjects

subjects = get_subjects()

print('총 ', len(subjects), '개의 타입을 찾았습니다.')

print(subjects)

conversations = []
i = 1
count = 1

# 모든 대화 주제 각각에 접근합니다.
for sub in subjects:
    print('(', i, '/', len(subjects), ') ', sub, ': ', len(conversations), "개")
    # 대화 스크립트를 보여주는 페이지로의 요청(Request) 객체를 생성합니다.
    req  = requests.get('http://basicenglishspeaking.com/' + sub.replace(" ", "-"))
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    qnas = soup.findAll('div',{"class": "sc_player_container1"})

    # 각각의 대화 내용에 모두 접근합니다.
    for qna in qnas:
        if qnas.index(qna) % 2 == 0:
            q = qna.next_sibling
        else:
            a = qna.next_sibling
            c = Conversation(sub, count, q, a)
            conversations.append(c)
            count = count + 1
    i = i + 1

print('총 ', len(conversations), '개의 대화를 찾았습니다.')

# 모든 대화 내용을 출력합니다.
for c in conversations:
    print(str(c))

# 자동화 테스트를 위해 셀레니움(Selenium)을 불러옵니다.
from selenium import webdriver

# 크롬 웹 드라이버의 경로를 설정합니다.
driver = webdriver.Chrome('C:\Chrome Driver\Chrome Driver.exe')

# 크롬을 통해 Paraphrase 서비스 사이트에 접속합니다.
driver.get('https://articlerewritertool.com/')

dic = {}
# conversations Length가 늘어나는 문제 해결 필요
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

# 모든 대화 내용을 출력합니다.
for c in conversations:
    print(str(c))
    
print('총 ', len(conversations), '개의 대화가 존재합니다.')

import xlsxwriter

# 엑셀 워크 북 및 워크 시트를 생성합니다.
workbook = xlsxwriter.Workbook('Conversation Data.xlsx')
worksheet = workbook.add_worksheet()

row = 0
col = 0

# 모든 대화 내용을 엑셀로 저장합니다.
for c in conversations:
    worksheet.write(row, col, c.contentName)
    worksheet.write(row, col + 1, c.contentType)
    worksheet.write(row, col + 2, c.question)
    worksheet.write(row, col + 3, c.answer)
    row = row + 1
    
workbook.close()

# -*- coding: utf-8 -*-

# Dialog Flow에 Import할 수 있는 Intent 파일로 출력하기
i = 1
# 출력, 입력 값 JSON 파일을 생성합니다.
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
        # 출력, 입력 값 JSON 파일을 생성합니다.
        prev = str(c.contentName) + str(c.contentType)
        f = open(prev + '.json', 'w', encoding='UTF-8')
        f.write('{ "id": "10d3155d-4468-4118-8f5d-15009af446d0", "name": "' + prev + '", "auto": true, "contexts": [], "responses": [ { "resetContexts": false, "affectedContexts": [], "parameters": [], "messages": [ { "type": 0, "lang": "ko", "speech": "' + c.answer + '" } ], "defaultResponsePlatforms": {}, "speech": [] } ], "priority": 500000, "webhookUsed": false, "webhookForSlotFilling": false, "fallbackIntent": false, "events": [] }')
        f.close()
        f = open(prev + '_usersays_ko.json', 'w', encoding='UTF-8')
        f.write("[")
        f.write('{ "id": "3330d5a3-f38e-48fd-a3e6-000000000001", "data": [ { "text": "' + c.question + '", "userDefined": false } ], "isTemplate": false, "count": 0 },')
    i = i + 1