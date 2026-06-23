# Классификатор для статей
## По категориям:
```
categories = [
    'rec.sport.hockey', 'rec.sport.baseball',
    'sci.space', 'sci.med',
    'comp.graphics', 'talk.politics.guns',
]
```

## EDA:
![Количество документов на класс]('https://github.com/Sanorian/post_classifier/blob/main/images/documents_count.png')
### Распределение по классам
```
category
0    973
1    994
2    999
3    990
4    987
5    910
Name: count, dtype: int64
Минимум: 910, максимум: 999
Разброс: 89
```
![Распределение длин текстов]('https://github.com/Sanorian/post_classifier/blob/main/images/length_words.png')
### Статистика длин текстов
```
count     5853.000000
mean       222.104562
std        516.844474
min          0.000000
25%         57.000000
50%        115.000000
75%        231.000000
max      11251.000000
```
### Топ-10 наиболее характерных слов для выбранных категорий
```
Категория: rec.sport.hockey
  hockey: 3198.90
  game: 2286.37
  nhl: 1766.64
  team: 1676.98
  25: 1564.23
  55: 1478.46
  pit: 1289.53
  det: 1284.63
  play: 1224.77
  la: 1224.16

Категория: sci.space
  space: 6662.36
  nasa: 2191.31
  launch: 1948.87
  earth: 1901.45
  shuttle: 1851.43
  orbit: 1716.68
  mission: 1565.56
  moon: 1380.97
  solar: 1329.90
  spacecraft: 1291.68

Категория: talk.politics.guns
  gun: 4870.21
  fbi: 2498.24
  guns: 2483.68
  fire: 1875.50
  firearms: 1591.54
  batf: 1529.81
  government: 1467.01
  weapons: 1440.92
  atf: 1399.45
  koresh: 1346.80
```
### Вывод
```
В каждой из трёх выбранных категорий в топ-10 входят очевидные тематические термины:
- rec.sport.hockey: ожидаемо присутствуют слова 'hockey', 'puck', 'goal', 'ice', 'team', 'game'.
- sci.space: явно выделяются 'space', 'orbit', 'launch', 'moon', 'astronaut', 'mission'.
- talk.politics.guns: доминируют 'gun', 'firearm', 'rights', 'rifle', 'control', 'weapon'.

Таким образом, слова-маркеры действительно являются наиболее характерными для своих категорий,
что подтверждает высокую различительную способность лексики в данном наборе данных.
```

## Результаты 3 ранов:
```
Run #1: tfidf-logreg: accuracy=0.9346, f1_macro=0.9346
Run #2: catboost-multiclass: acc=0.8961, f1=0.8965
Run #3: logreg-gridsearch: best_params={'max_features': 40000, 'C': 5}, acc=0.9372, f1=0.9372
```

## Confusion Matrix и анализ ошибок:
```
Результаты запусков:
    tfidf-logreg: f1_macro = 0.9346
    catboost-multiclass: f1_macro = 0.8965
    logreg-gridsearch: f1_macro = 0.9372

Лучшая модель: logreg-gridsearch (f1_macro = 0.9372)
```
![Confusion matrix]('https://github.com/Sanorian/post_classifier/blob/main/images/confusion_matrix.png')

### Топ-3 пары классов, которые модель путает чаще всего (нормализованная доля ошибок):
```
    rec.sport.baseball -> sci.space: 0.053 (доля ошибочных предсказаний для класса rec.sport.baseball)
    comp.graphics -> sci.med: 0.038 (доля ошибочных предсказаний для класса comp.graphics)
    comp.graphics -> rec.sport.hockey: 0.030 (доля ошибочных предсказаний для класса comp.graphics)
```

## Для запуска приложения:
```
https://github.com/Sanorian/post_classifier.git
docker-compose up
```