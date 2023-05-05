import datetime as date, os
os.system("cls")
rgb = lambda r,g,b: f"\u001b[38;2;{r};{g};{b}m"
types = {"!":rgb(255,187,51),"+":rgb(0,200,81),"-":rgb(255,68,68),"i":rgb(51,181,229)}
now = lambda: f"[{date.datetime.now().strftime('%H:%M:%S')}] "
msg = lambda type, text, time=1: f"{types[type]}» {now() if time else ''}{text}" + f"\u001b[0m"