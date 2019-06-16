import os
py1=os.popen('python realrt.py')
os.system('./pfcount -i ens33')
py2=os.popen('python realrt.py')
print(int(py2.read())-int(py1.read()))
