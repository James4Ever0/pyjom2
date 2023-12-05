# Pyjom2

*Media automation, reimagined.*

The old repository is simply bloated, no way to fix.

We simply create a new one instead. Write some scripts that may step into the old repository, copy some files, back and forth.

Subrepositories shall just be ignored, added to .gitignore, with some scripts that anyone can clone them back into relative places.

You may change something crucial in subrepositories, and that is important. We may apply patch over original repository.

Ask the ChatGPT on how to manage a giant repository? Had better not to commit multiple files, multiple subrepositories, big binary files, refuse to do so when such problem detected, right before things go sour, and fix it yourself.

I may integrate that warning feature into `git_atomic_commit`.
