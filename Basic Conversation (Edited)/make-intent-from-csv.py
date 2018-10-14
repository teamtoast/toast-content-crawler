import openpyxl

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

# ���� ��ȭ �����Ͱ� ��� ���� ������ ���ϴ�.
wb = openpyxl.load_workbook('Conversation Data.xlsx')
 
# Ȱ�� ��Ʈ�� ����ϴ�.
ws = wb.active

conversations = []

# ��Ʈ ���� �����ϴ� ��� ���� ��ȭ �����͸� ��ü�� ����ϴ�.
for r in ws.rows:
    c = Conversation(r[0].value, r[1].value, r[2].value, r[3].value)
    conversations.append(c)
    
wb.close()

for c in conversations:
    print(str(c))
    
# ��� ��ȭ ������ ����մϴ�.
for c in conversations:
    print(str(c))
    
print('�� ', len(conversations), '���� ��ȭ�� �����մϴ�.')

# -*- coding: utf-8 -*-

# ���Ϸ� ����ϱ�
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