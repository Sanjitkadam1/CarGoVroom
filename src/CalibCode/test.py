x =[0,1,2,3,54,2]
i = 0 
while i<len(x):
    if x[i]>20:
        x.pop(i)
    i+=1

print(x)