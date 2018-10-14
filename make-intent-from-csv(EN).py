import openpyxl

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

# 영어 대화 데이터가 담긴 엑셀 파일을 엽니다.
wb = openpyxl.load_workbook('Conversation Data.xlsx')
 
# 활성 시트를 얻습니다.
ws = wb.active

conversations = []

# 시트 내에 존재하는 모든 영어 대화 데이터를 객체로 담습니다.
for r in ws.rows:
    c = Conversation(r[0].value, r[1].value, r[2].value, r[3].value)
    conversations.append(c)
    
wb.close()

for c in conversations:
    print(str(c))
    
# 모든 대화 내용을 출력합니다.
for c in conversations:
    print(str(c))
    
print('총 ', len(conversations), '개의 대화가 존재합니다.')

# -*- coding: utf-8 -*-

# 파일로 출력하기
i = 1
# 출력, 입력 값 JSON 파일을 생성합니다.
prev = str(conversations[0].contentName) + str(conversations[0].contentType)
f = open(prev + '.json', 'w', encoding='UTF-8')
f.write('{ "id": "10d3155d-4468-4118-8f5d-15009af446d0", "name": "' + prev + '", "auto": true, "contexts": [], "responses": [ { "resetContexts": false, "affectedContexts": [], "parameters": [], "messages": [ { "type": 0, "lang": "en", "speech": "' + conversations[0].answer + '" } ], "defaultResponsePlatforms": {}, "speech": [] } ], "priority": 500000, "webhookUsed": false, "webhookForSlotFilling": false, "fallbackIntent": false, "events": [] }')
f.close()
f = open(prev + '_usersays_en.json', 'w', encoding='UTF-8')
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
        f.write('{ "id": "10d3155d-4468-4118-8f5d-15009af446d0", "name": "' + prev + '", "auto": true, "contexts": [], "responses": [ { "resetContexts": false, "affectedContexts": [], "parameters": [], "messages": [ { "type": 0, "lang": "en", "speech": "' + c.answer + '" } ], "defaultResponsePlatforms": {}, "speech": [] } ], "priority": 500000, "webhookUsed": false, "webhookForSlotFilling": false, "fallbackIntent": false, "events": [] }')
        f.close()
        f = open(prev + '_usersays_en.json', 'w', encoding='UTF-8')
        f.write("[")
        f.write('{ "id": "3330d5a3-f38e-48fd-a3e6-000000000001", "data": [ { "text": "' + c.question + '", "userDefined": false } ], "isTemplate": false, "count": 0 },')
    i = i + 1