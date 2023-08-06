'''
Facts API module (famo)
'''

def get_fact():
    from requests import get
    fact = get(url='https://elian.pythonanywhere.com/api').json()
    return fact['fact']

def get_fact_json():
    from requests import get
    fact = get(url='https://elian.pythonanywhere.com/api').json()
    return fact
