
# -*- coding: utf-8 -*- #

# In[187]:


from bs4 import BeautifulSoup
import requests

# 한 건의 대화에 대한 정보를 담는 객체입니다.
class Conversation:
    # 질문(Question), 응답(Answer) 두 변수로 구성됩니다.
    def __init__(self, contentName, contentType, question, answer):
        if len(question) > 0 and question[0] == ':':
            question = question[1:]
        if len(answer) > 0 and answer[0] == ':':
            answer = answer[1:]
        while len(question) > 0 and question[0] == ' ':
            question = question[1:]
        while len(answer) > 0 and answer[0] == ':':
            answer = answer[1:]
        self.contentName = contentName
        self.contentType = contentType
        self.question = question
        self.answer = answer
        
    def __str__(self):
        return "질문: " + self.question + "\n답변: " + self.answer + "\n"

# 한 건의 영어 대화 주제 링크를 담는 객체입니다.
class Subject:
    def __init__(self, number, title, link):
        self.number = number
        self.title = title
        self.link = link
        
    def __str__(self):
        return "번호: " + self.number + "\n제목: " + self.title + "\n답변: " + self.link + "\n"
    
# 모든 영어 대화 주제를 추출하는 함수입니다.
def get_subjects(number):
    subjects = []
    
    req = requests.get('http://www.elllo.org/english/' + number)
    html = req.text
    
    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.findAll('div', {"class": "mobilelist"})
    
    for subject in divs:
        tags = subject.findAll('a')
        
        for tag in tags:
            title = tag.text
            if title == '':
                continue
            link = tag['href']
            s = Subject(number, title, link)
            # print(s) # 추출된 주제를 출력합니다.
            subjects.append(s)
            
    return subjects

# 특정 대화 주제의 대화 내용을 크롤링합니다.
def get_conversation(number, url):
    conversations = []
    
    req = requests.get('http://www.elllo.org/english/' + number + "/" + url)
    html = req.text
    
    soup = BeautifulSoup(html, 'html.parser')
    if soup.text.find("transcript") != -1: # 스크립트 자체가 페이지에 없으면 취소
        return conversations
    if len(soup.findAll('div', {"class": "transcript"})) < 1:
        return conversations
    sayings = soup.findAll('div', {"class": "transcript"})[0]
    strongs = sayings.findAll('strong') # strong에 들어간 사람 이름 정보 확인

    idx = 0
    while True:
        if idx + 1 >= len(strongs):
            break
        question = strongs[idx].nextSibling # 사람 이름 다음에 메시지가 등장
        answer = strongs[idx + 1].nextSibling
        idx = idx + 1
        if question == None or answer == None:
            continue
        c = Conversation(number, idx, str(question), str(answer))
        print(c) # 추출된 대화 내용을 출력합니다.
        conversations.append(c)
        
    return conversations


# In[188]:


subjects = []

# 모든 영어 대화 주제 링크를 얻어냅니다.
for i in range(0, 10):
    print("(" + str(i) + " / " + str(9) + ")")
    subjects.extend(get_subjects(str(1001 + (i * 50))))

print("전체 대화 주제의 개수는 " + str(len(subjects)) + "개 입니다.")


# In[189]:


conversations = []

idx = 0
# 모든 대화 내용을 얻어냅니다.
for subject in subjects:
    print("(" + str(idx) + "/" + str(len(subjects)) + ") 현재 주제: " + subject.title + "\n")
    conversations.extend(get_conversation(subject.number, subject.link))
    idx = idx + 1
    
print("전체 대화 주제의 개수는 " + str(len(conversations)) + "개 입니다.")


# In[191]:


import xlsxwriter

# 엑셀 워크 북 및 워크 시트를 생성합니다.
workbook = xlsxwriter.Workbook('Conversation Data 1.xlsx')
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


# In[ ]:


# 내보내기 이후에 엑셀에서 공백이 있거나 None으로 처리된 것들은 제거합니다.

