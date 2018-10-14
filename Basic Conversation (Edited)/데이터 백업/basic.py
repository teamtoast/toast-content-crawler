
# -*- coding: utf-8 -*- #

# In[187]:


from bs4 import BeautifulSoup
import requests

# �� ���� ��ȭ�� ���� ������ ��� ��ü�Դϴ�.
class Conversation:
    # ����(Question), ����(Answer) �� ������ �����˴ϴ�.
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
        return "����: " + self.question + "\n�亯: " + self.answer + "\n"

# �� ���� ���� ��ȭ ���� ��ũ�� ��� ��ü�Դϴ�.
class Subject:
    def __init__(self, number, title, link):
        self.number = number
        self.title = title
        self.link = link
        
    def __str__(self):
        return "��ȣ: " + self.number + "\n����: " + self.title + "\n�亯: " + self.link + "\n"
    
# ��� ���� ��ȭ ������ �����ϴ� �Լ��Դϴ�.
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
            # print(s) # ����� ������ ����մϴ�.
            subjects.append(s)
            
    return subjects

# Ư�� ��ȭ ������ ��ȭ ������ ũ�Ѹ��մϴ�.
def get_conversation(number, url):
    conversations = []
    
    req = requests.get('http://www.elllo.org/english/' + number + "/" + url)
    html = req.text
    
    soup = BeautifulSoup(html, 'html.parser')
    if soup.text.find("transcript") != -1: # ��ũ��Ʈ ��ü�� �������� ������ ���
        return conversations
    if len(soup.findAll('div', {"class": "transcript"})) < 1:
        return conversations
    sayings = soup.findAll('div', {"class": "transcript"})[0]
    strongs = sayings.findAll('strong') # strong�� �� ��� �̸� ���� Ȯ��

    idx = 0
    while True:
        if idx + 1 >= len(strongs):
            break
        question = strongs[idx].nextSibling # ��� �̸� ������ �޽����� ����
        answer = strongs[idx + 1].nextSibling
        idx = idx + 1
        if question == None or answer == None:
            continue
        c = Conversation(number, idx, str(question), str(answer))
        print(c) # ����� ��ȭ ������ ����մϴ�.
        conversations.append(c)
        
    return conversations


# In[188]:


subjects = []

# ��� ���� ��ȭ ���� ��ũ�� �����ϴ�.
for i in range(0, 10):
    print("(" + str(i) + " / " + str(9) + ")")
    subjects.extend(get_subjects(str(1001 + (i * 50))))

print("��ü ��ȭ ������ ������ " + str(len(subjects)) + "�� �Դϴ�.")


# In[189]:


conversations = []

idx = 0
# ��� ��ȭ ������ �����ϴ�.
for subject in subjects:
    print("(" + str(idx) + "/" + str(len(subjects)) + ") ���� ����: " + subject.title + "\n")
    conversations.extend(get_conversation(subject.number, subject.link))
    idx = idx + 1
    
print("��ü ��ȭ ������ ������ " + str(len(conversations)) + "�� �Դϴ�.")


# In[191]:


import xlsxwriter

# ���� ��ũ �� �� ��ũ ��Ʈ�� �����մϴ�.
workbook = xlsxwriter.Workbook('Conversation Data 1.xlsx')
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


# In[ ]:


# �������� ���Ŀ� �������� ������ �ְų� None���� ó���� �͵��� �����մϴ�.

