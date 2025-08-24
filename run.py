import sys, subprocess
python_bin = "venv/bin/python"

def run_tool(path, args):
    subprocess.run([python_bin, path, args])

def main(args):
    if str(args[1]).lower() == "booru":
        run_tool("booru_tools/gelbooru.py")
        return
    elif str(args[1]).lower() == "pixiv":
        run_tool("pixiv_tools/pixiv.py", str(args[2]))
        return
    elif str(args[1]).lower() == "twitter":
        run_tool("twitter_tools/twitter.py", str(args[2]))
        return
    





    elif str(args[1]).lower() == "bulk":
        return
    else:
        print("Invalid input:\n" + args)

main(sys.argv)