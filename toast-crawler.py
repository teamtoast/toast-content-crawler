from bs4 import BeautifulSoup
import requests
import pymysql

def get_subjects():
    subjects = []

    req  = requests.get('https://basicenglishspeaking.com/daily-english-conversation-topics/')
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    divs = soup.findAll('div',{"class": "su-column-inner"})
    for div in divs:
        subtags = div.findAll('a')

        for subtag in subtags:
            sub = subtag.text
            subjects.append(sub)
    
    return subjects

    
conn = pymysql.connect(host='localhost', user='root', password='',db='mydb', charset='utf8')
curs = conn.cursor(pymysql.cursors.DictCursor)

sql = """INSERT INTO `STUDY_CONTENT` (`contentName`, `question`, `answer`) 
        VALUES(%s, %s, %s)"""

subjects = get_subjects()

for sub in subjects:
    print('>>' + sub + '\n')
    req  = requests.get('http://basicenglishspeaking.com/' + sub)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    qnas = soup.findAll('div',{"class": "sc_player_container1"})


    for qna in qnas:
        if qnas.index(qna) % 2 == 0:
            q = qna.next_sibling
        else:
            a = qna.next_sibling
            curs.execute(sql,(sub,q,a))
            # print(sub + "," + q + "," + a)

conn.commit()
conn.close()

