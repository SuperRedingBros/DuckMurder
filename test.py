import git
import os

file = "temp/temp"

if(not os.path.exists(file)):
    repo = git.Repo.clone_from('https://github.com/SuperRedingBros/Packs-Of-DOOM-.git', file)
else:
    repo = git.Repo(file)



print(repo.remotes.origin.pull())
repo.close()
quit()
