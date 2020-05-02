import os

path="C:\dataset\Politifact\\temp1"
for fname in os.listdir(path):
    li=fname.split(".")
    if li[0][-2]==" ":
        li[0]=li[0].replace(li[0][-1],"0"+li[0][-1])
        #print("{:02d}".format(int(li[0][-1])))
        dst=".".join(li)
        print(dst)
        os.rename(os.path.join(path,fname), os.path.join(path,dst))

#print("{:02d}".format(2))





