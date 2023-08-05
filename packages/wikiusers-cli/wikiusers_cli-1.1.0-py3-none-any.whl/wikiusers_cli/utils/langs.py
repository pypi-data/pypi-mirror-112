from whaaaaat import prompt

def select_languages(available_langs: list[str], current_langs: list[str]) -> list[str]:
    current_langs = [l for l in current_langs]

    include_all = 'all' in current_langs
    if include_all:
        current_langs.remove('all')

    options = [
        {'name': option, 'value': option,
            'checked': include_all or option in current_langs}
        for option in available_langs
    ]
    answer = prompt({
        'name': 'langs',
        'message': 'Select the languages to purge',
        'type': 'checkbox',
        'choices': options
    })
    return answer['langs']