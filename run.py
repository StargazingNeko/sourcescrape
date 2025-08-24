import sys, subprocess, os
python_bin = os.getcwd()+"/venv/bin/python"

def run_tool(path, args, count = 0):
    subprocess.run([python_bin, path, args])

def Gelbooru(args):
    os.chdir(os.getcwd()+"/gelbooru_tools")
    run_tool("gelbooru.py", "")

def Pixiv(args):
    os.chdir(os.getcwd()+"/pixiv_tools/")
    run_tool("pixiv.py", str(args))

def Twitter(args):
    os.chdir(os.getcwd()+"/twitter_tools")
    run_tool("twitter.py", str(args))

def Nijie(args):
    os.chdir(os.getcwd()+"/nijie_tools")
    run_tool("nijie.py", str(args))

def main(args):
    if str(args[1]).lower() == "booru" or str(args[1]).lower() == "gelbooru":
        Gelbooru(args[2])
        return
    elif str(args[1]).lower() == "pixiv":
        Pixiv(args[2])
        return
    elif str(args[1]).lower() == "twitter":
        Twitter(args[2])
        return
    elif str(args[1]).lower() == "nijie":
        Nijie(args[2])
        return
    


    elif str(args[1]).lower() == "bulk":
        print("Not implimented yet.")
        return
    else:
        print("Invalid input:\n" + args)

main(sys.argv)
