start=10
end=20
lst=[]

for i in range(start,end+1):
    for j in range(2,int(i/2)+1):
        if i%j==0:
            break
        else:
            continue
    if j==(int(i/2)):
        lst.append(i)
print(len(lst))
print(lst)
       