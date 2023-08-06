#!/usr/bin/env python
import random
import os
import sys

update = (random.randint(-1,-1))
upgrade = (random.randint(-2,-2))
updateupgrade = (random.randint(-3,-3))
git = (random.randint(-4,-4))
help = (random.randint(-8,-8))
break0 = (random.randint(-0,-0))

print("For help type -8 at the end!")
while True:
        odg = input("Type command:")
        try:
            odg = int(odg)
            if odg == update:
                print("I start updating!")
                print("Type password for update!")
                os.system('sudo apt update')
            if odg == upgrade:
                print("I start upgrading!")
                os.system('sudo apt upgrade')
            if odg == updateupgrade:
                print("I start updating and upgrading!")
                os.system('sudo apt update')
                os.system('sudo apt upgrade')
            if odg == help:
                print("I open the help!")
                print("To update tipe -1.Type -2 for upgrade. Type -3 for update and upgrade. Type -4 for git repo download. Need help? Type -8 for it! Type -0 for stop! Copyrighting by Julij Dominik Mrak.")
            if odg == git:
                print("I clone some folders and files from git repo...")
                os.system('sudo apt update')
                os.system('sudo apt install git')
                os.system('git clone https://github.com/pro1mantis/UPapp/tree/main/git-clone')
                print("Go to the git-clone folder. Open file named git-clone.py and type to the os.system git clone your repo! And run it! OK?")
                break
            if odg == break0:
                print("OK I stop...")
                sys.exit()
                break
        except ValueError:
            print("That isn't a command!")
