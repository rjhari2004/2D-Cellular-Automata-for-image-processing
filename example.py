import numpy as np
import pandas as pd
def apply_colors(val):
    color = ''
    if val == 0:
        color = 'background-color: white'
    elif val==1:
        color = 'background-color: yellow'
    elif val==2:
        color='background-color: red'
    elif val==3:
        color='background-color: green'
    elif val==4:
        color='background-color: blue'
    elif val==5:
        color='background-color: brown'
    elif val==6:
        color='background-color: grey'
    elif val==7:
        color='background-color: orange'
    return color
n=int(input("Enter the grid size :"))
a=[[column for column in range(n)] for row in range(n)]
b=[[column for column in range(n)] for row in range(n)]
for i in range(n):
    for j in range(n):
        a[i][j]=b[i][j]=0
row,col=map(int,input("Enter image Dimensions :").split())
print("Enter the image :")
for i in range(20,row+20):
    for j in range(20,col+20):
        a[i][j]=int(input())
np_a=np.array(a)
DF=pd.DataFrame(np_a)
styled_df = DF.style.applymap(apply_colors)
styled_df.to_excel('Initial.xlsx', engine='openpyxl', index=False)
step=int(input("Enter steps:"))
for m in range(step):
    for i in range(n):
        for j in range(n):
            if(i-1>=0 and j-1>=0 and i+1<n and j+1<n):
                b[i][j]=(a[i][j]+a[i][j+1]+a[i+1][j+1])%8
    a=b
    np_a=np.array(a)
    DF=pd.DataFrame(np_a)
    styled_df = DF.style.applymap(apply_colors)
    styled_df.to_excel(f'Step{m+1}.xlsx', engine='openpyxl', index=False)
