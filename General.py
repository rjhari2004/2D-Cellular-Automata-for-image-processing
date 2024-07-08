import numpy as np
import pandas as pd
def xor(ini_dictionary1,ini_dictionary2):
    final_dictionary = {}
    for key in ini_dictionary1:
        final_dictionary[key] = ini_dictionary1[key] + ini_dictionary2.get(key, 0)
    for key in ini_dictionary2:
        if key not in final_dictionary:
            final_dictionary[key] = ini_dictionary2[key]
    return final_dictionary
n=int(input("Enter the grid size :"))
a=[[column for column in range(n)] for row in range(n)]
b=[[column for column in range(n)] for row in range(n)]
for i in range(n):
    for j in range(n):
        a[i][j]=dict()
        b[i][j]=dict()
row,col=map(int,input("Enter image dimension :").split())
print("Enter the image :")
for i in range(20,row+20):
    for j in range(20,col+20):
        s=input()
        a[i][j][s]=1
        b[i][j][s]=1
step=int(input("Enter the number of steps :"))
for m in range(1,step+1):
    print("Step number :",m)
    for i in range(0,n):
        for j in range(0,n):
            if i-1>=0 and j-1>=0 and i+1<n and j+1<n:
               b[i][j]=xor(a[i+1][j-1],a[i+1][j])
               b[i][j]=xor(b[i][j],a[i+1][j+1])
            #    b[i][j]=xor(b[i][j],a[i+1][j+1])
            #    b[i][j]=xor(b[i][j],a[i+1][j])
            #    b[i][j]=xor(b[i][j],a[i+1][j-1])
            #    b[i][j]=xor(b[i][j],a[i][j-1])
            #    b[i][j]=xor(b[i][j],a[i-1][j-1])
    for i in range(0,n):
        for j in range(0,n):
            a[i][j]=b[i][j]
    display=[[column for column in range(n)] for row in range(n)]
    display2=[[column for column in range(n)] for row in range(n)]
    for i in range(0,n):
        for j in range(0,n):
            display[i][j]=""
            display2[i][j]=""
    for i in range(0,n):
        for j in range(0,n):
            it=0
            bit=0
            for key in a[i][j]:
                if bit!=0:
                        display[i][j]+="^"+str(a[i][j][key])+str(key)
                else:
                        display[i][j]+=str(a[i][j][key])+str(key)
                bit+=1 
                if a[i][j][key]%2==0:
                    display2[i][j]+=""
                else:
                    if it!=0:
                        display2[i][j]+="^"+str(a[i][j][key])+str(key)
                    else:
                        display2[i][j]+=str(a[i][j][key])+str(key)
                    it+=1 
    for i in range(0,n):
        for j in range(0,n):
            print(display2[i][j],end=" ")
        print()
    display_np_1=np.array(display)
    display_np_2=np.array(display2)
    DF = pd.DataFrame(display_np_1) 
    DF.to_csv(f"data1{m}.csv")
    DF=pd.DataFrame(display_np_2)
    DF.to_csv(f"data2{m}.csv")

    #print(display_np)
