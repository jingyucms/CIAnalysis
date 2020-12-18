import subprocess


def main():

        with open("files.txt") as f:
                content = f.readlines()
        content = [x.strip() for x in content] 
        for line in content:
                if ".root" in line:
                        command = ['xrdcp', 'root://cmseos.fnal.gov///store/user/cmsdas/2021/long_exercises/CI//'+line,"."]
                        print command
                        subprocess.call(command)
main()
