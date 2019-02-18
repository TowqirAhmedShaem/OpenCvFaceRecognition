import os
os.system("/home/pi/gitlab/FaceAccessControl")
os.system("git status")
os.system("git add .")
commit = "Shaem"
os.system("git commit -m "+commit)
os.system("git push origin TestShaem")

