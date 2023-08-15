import requests
import argparse
import zipfile
import os

# GLOBAL VARIABLES
programName = "proPkg"
programDesc = "a simple packagemanager"
reposLink = "https://led-reamer.github.io/libs/"
libsFile = "libs.txt"
libList = []

#ARGUMENTS
argParser = argparse.ArgumentParser(prog=programName, description=programDesc, epilog="")

#argParser.add_argument("mode", choices=["list", "find", "get"], type=str, help="list all packages, search for specific names, download a package")
argParser.add_argument("-l", "--list", action='store_true', required=False)
argParser.add_argument("-f", "--find", type=str, required=False)
argParser.add_argument("-g", "--get", type=str, required=False)
args = argParser.parse_args()


def getList():
    global libList
    libList = requests.get(reposLink + libsFile).text.splitlines()


getList()

if(args.list):
    print(libList)
    exit()

if(args.find):
    if(args.find == None):
        print(libList)
        exit()
    print([s for s in libList if args.find in s])
    exit()

if(args.get):
    if(not args.get in libList):
        print("Could not find \"" + args.get + "\"")
        print(libList)
        exit()
    
    open(args.get, 'wb').write(requests.get(reposLink + args.get, allow_redirects=True).content)
    
    if(args.get.endswith(".zip")):
        with zipfile.ZipFile(args.get, 'r') as zip_ref:
            zip_ref.extractall(".")
        os.remove(args.get)
    exit()
    

#if no accepted mode was detected
argParser.print_help()