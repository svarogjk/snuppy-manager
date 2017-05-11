import requests


def get_changes(url):
    'https://github.com/request/request/blob/master/CHANGELOG.md'
    changes_url = url + '/blob/master/CHANGELOG.md'
    if requests.head(changes_url).ok:
        return changes_url
    else:
        return 'CHANGELOG.md not found in master branch'

if __name__ == '__main__':
    url = get_changes('https://github.com/request/request')
    print(url)