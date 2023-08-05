class MainPrompt:
    def __init__(self):
        pass
    def scrm(self, cmd):
        import os
        os.system(cmd)
    def lrgd(self):
        print(self)
prompt = MainPrompt()
prompt.scrm("echo PyTools Prompt [copyright KareemTheBest] 2021.")
prompt.scrm("color 0A")
prompt.scrm("cmd.exe /k prompt $D $P$G")
