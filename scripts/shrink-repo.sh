#!usr/bin/env/ bash

# poetry add git-filter-repo
# cp -r fitness-tracker fitness-tracker-backup

# Get 40 largest files
git rev-list --objects --all | grep "$(git verify-pack -v .git/objects/pack/*.idx | sort -k 3 -n | tail -40 | awk '{print$1}')"

# git filter-repo --invert-paths --force --path dist/ --path docs/project_docs/img/
# git filter-repo --invert-paths --force --path poetry.lock

# git reflog expire --expire=now --all

# git gc --prune=now --aggressive

# git remote add origin https://github.com/TheNewThinkTank/fitness-tracker.git

# git push --force --all

# git remote -v
