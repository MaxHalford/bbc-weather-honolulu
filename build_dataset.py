from git import Repo

repo = Repo('.')

DATA_BRANCH = 'data'
FILE_NAME = 'latest_forecast.json'

for commit in repo.iter_commits(DATA_BRANCH):
    try:
        blob = [b for b in commit.tree.blobs if b.name == FILE_NAME][0]
    except IndexError:
        continue
    print(blob.data_stream.read().decode('utf8'))
    break
