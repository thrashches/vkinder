def get_criteriums_from_console_input() -> dict:
    search_criteriums = {}
    print('===== Поиск людей в vk =====')
    print('Для выхода введите "q"')
    if city := input('Город: '):
        search_criteriums['city'] = city

    if status := input('''Семейное положение, варианты:
        • 1 — не женат (не замужем),
        • 2 — встречается,
        • 3 — помолвлен(-а),
        • 4 — женат(замужем),
        • 5 — всё сложно,
        • 6 — в активном поиске,
        • 7 — влюблен(-а),
        • 8 — в гражданском браке.
    \nВведите вариант ответа: '''):
        if status == 'q':
            quit()
        search_criteriums['status'] = int(status)
    if sex := input('''Пол, варианты:
        • 1 — женщина,
        • 2 — мужчина,
        • 0 — любой (по умолчанию).
    \nВведите вариант ответа: '''):
        if sex == 'q':
            quit()
        search_criteriums['sex'] = int(sex)

    if age_from := input('Возраст от: '):
        if age_from == 'q':
            quit()
        search_criteriums['age_from'] = int(age_from)
    if age_to := input('Возраст до: '):
        if age_to == 'q':
            quit()
        search_criteriums['age_to'] = int(age_to)
    return search_criteriums
