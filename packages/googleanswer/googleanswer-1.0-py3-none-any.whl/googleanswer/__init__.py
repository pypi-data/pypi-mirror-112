import requests
def google(q):
    res= requests.get('http://api.sanatgarg.com/google_search/answers.php?q='+q)
    res = (res.text).split("push('")[1].split("'")[0]
    res = res.split('�')
    res = ((' ').join(res))
    return res
