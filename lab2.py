import csv
import requests
from bs4 import BeautifulSoup

dialog = {
    'phrase1': ['Вас приветствует помощник, который подберет вам аниме. Для этого ответьте на несколько вопросов. '],
    'phrase2': ['Заполняйте на английском, пожалуйста.'],
    'phrase3': ['Если ответ на вопрос не важен, оставьте поле пустым (нажмите Enter)'],
    'questions': ('Какой жанр вас интересует?',
                  'Какой формат аниме вас устроит?',
                  'Какое минимальное количество эпизодов?',
                  'Аниме должно быть закончено? Введите True или False.',
                  'Какой год начала съемки аниме вас интересует?',
                  'Какой год окончания съемки аниме вас интересует?',
                  'Какая студия вас интересует?',
                  )
}

question = (
    'Tags',
    'Type',
    'Episodes',
    'Finished',
    'StartYear',
    'EndYear',
    'Studios'
)

answer = {
    'Tags': '',
    'Type': '',
    'Episodes': '',
    'Finished': '',
    'StartYear': '',
    'EndYear': '',
    'Studios': ''
}


def dialog_sequence(dialog, question):
    print(*dialog['phrase1'])
    print(*dialog['phrase2'])
    print(*dialog['phrase3'])
    questions = dialog['questions']
    for k in range(len(questions)):
        print(questions[k])
        answer[question[k]] = input()


dialog_sequence(dialog, question)
anime_list = []
with open('anime.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        acceptable = True
        for k in question:
            if answer[k] != '':
                if (k == 'Tags') or (k == 'Studios'):
                    list = row[k].split(', ')
                    answer_list = answer[k].split(', ')
                    if set(answer_list).issubset(set(list)):
                        acceptable = acceptable and True
                    else:
                        acceptable = acceptable and False
                if (k == 'Type') or (k == 'Finished') or (k == 'StartYear') or (k == 'EndYear'):
                    if answer[k] == row[k]:
                        acceptable = acceptable and True
                    else:
                        acceptable = acceptable and False
                if k == 'Episodes':
                    if row[k] == 'Unknown':
                        episodes = float(0)
                    else:
                        episodes = float(row[k])
                    if episodes >= float(answer[k]):
                        acceptable = acceptable and True
                    else:
                        acceptable = acceptable and False
        if acceptable:
            if row['Rating Score'] == 'Unknown':
                anime_list.append([float(0), row['Url'], row['Name']])
            else:
                anime_list.append([float(row['Rating Score']), row['Url'], row['Name']])
anime_list.sort()
anime_list.reverse()

f = open('answer.txt', 'w', encoding='utf-8')
for i in range(min(5, len(anime_list))):
    response = requests.get(anime_list[i][1])
    soup = BeautifulSoup(response.text, 'html.parser')
    img = requests.get("https://www.anime-planet.com/" + soup.find('img', class_='screenshots')['src'])
    img_file = open(str(i + 1) + '.jpg', 'wb')
    img_file.write(img.content)
    img_file.close()
    f.write(anime_list[i][2] + ': ' + anime_list[i][1] + '\n')
for i in range(min(5, len(anime_list)), len(anime_list)):
    f.write(anime_list[i][2] + ': ' + anime_list[i][1] + '\n')
f.close()

print('--------------------------------------')
print('Подбор окончен. Аниме отсортированы в порядке убывания их рейтинга и находятся в файле answer.txt.')
print('Для первых 5 аниме с лучшим рейтингом вы можете посмотреть постеры.')
