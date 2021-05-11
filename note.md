# Note for this project

## Github actions

1. When push on this repo with a `prefix {section} {filename} - {message}`
2. Auto update readme with the new tool.

> `prefix` could be an emote, like 🤖

```
$ git add scripts/python/createRepo.py scripts/python/utils.py
$ git commit -m "🤖 script createRepo - help create new github repository from shell"
$ git push origin master
```