

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
import os

arr = os.listdir('C:\\Users\\palad\\opencv\\build\\x64\\vc14\lib')
names=[]
for name in arr:
    if "d.lib" in name:
        names.append(name)
        print(name)
