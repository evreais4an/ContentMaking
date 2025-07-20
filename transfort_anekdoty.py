with open("anekdoty.txt", "r", encoding="utf-8") as a:
    text = a.read()

e = ""
for i in text.split("\n"):
    if i == "":
        continue
    if i.isdigit():
        e += "***\n"
    else:
        e += i + "\n"

end = e.split("***")

with open("ee.txt", "w", encoding="utf-8") as a2:
    for part in end:
        a2.write(part.strip() + "\n---\n")
