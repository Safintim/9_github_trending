import requests
import datetime


def main():
    try:
        print('Топ 20-репозиториев за прошедшую неделю и количество открытых issues')
        for repo_owner, repo_name in get_trending_repositories(top_size=20):
            print(get_open_issues_amount(repo_owner, repo_name))
    except requests.exceptions.RequestException as e:
        exit(e)


def get_trending_repositories(top_size):
    last_week = datetime.date.today() - datetime.timedelta(days=7)

    url = 'https://api.github.com/search/repositories'
    params = {
        'q': 'created:>{}'.format(last_week),
        'sort': 'stars',
        'per_page': str(top_size)
    }
    response = requests.get(url, params=params)
    response.raise_for_status()

    for repo in response.json()['items']:
        yield (
            repo['owner']['login'],
            repo['name'],
        )


def get_open_issues_amount(repo_owner, repo_name):
    url = 'https://api.github.com/repos/{}/{}/'.format(repo_owner, repo_name)
    response = requests.get(url)
    response.raise_for_status()
    repo = response.json()
    return repo['open_issues_count'], repo['html_url']


if __name__ == '__main__':
    main()
