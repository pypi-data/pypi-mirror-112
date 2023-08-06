class Logger:
    colors = {
        "header": '\033[95m',
        "okBlue": '\033[94m',
        "okCyan": '\033[96m',
        "okGreen": '\033[92m',
        "warning": '\033[93m',
        "fail": '\033[91m',
        "endc": '\033[0m',
        "bold": '\033[1m',
        "underline": '\033[4m'
    }

    def log(self, color, text):
        print(self.colors[color] + text + self.colors['endc'])
