import os

entries = os.listdir('records2')
infolist = []
matlist = []
for i in entries:
    if "info" in i:
        infolist.append(i)
    else:
        matlist.append(i)


def num_finder(file_name):
    stringer = ""
    for i in file_name:
        if i == ".":
            break
        else:
            stringer += i
    return (stringer)

names = []
for i in entries:
    names.append(num_finder(i))
keep_list = []
for i in range(len(names)):
    for j in range(i+1, len(names)):
        if names[i] == names[j]:
            keep_list.append(names[i] + ".info")
            keep_list.append(names[i] + ".mat")

for i in entries:
    if i not in keep_list:
        os.remove("records2/" + i)


