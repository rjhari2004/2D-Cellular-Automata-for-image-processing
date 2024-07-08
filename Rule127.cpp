#include<bits/stdc++.h>
using namespace std;
int main()
{
    int a[100][100],b[100][100],n,step,i,j,row,col;
    cout<<"Enter the grid size :";
    cin>>n;
    for(i=0;i<n;i++)
    {
        for(j=0;j<n;j++)
        {
            a[i][j]=0;
            b[i][j]=0;
        }
    }
    cout<<"Enter image dimensions :";
    cin>>row>>col;
    cout<<"Enter the image :\n";
    for(i=19;i<19+row;i++)
    {
        for(j=20;j<20+col;j++)
        cin>>a[i][j];
    }
    cout<<"Entered image :\n";
    for(i=0;i<n;i++)
    {
        for(j=0;j<n;j++)
        {
            cout<<a[i][j]<<" ";
        }
        cout<<"\n";
    }
    cout<<"Enter steps :";
    cin>>step;
    int no=1;
    cout<<"Rule 127 :\n";
    while(step--)
    {
        cout<<"Step "<<no<<"\n";
        for(i=0;i<n;i++)
        {
            for(j=0;j<n;j++)  
            {
                if(i-1>=0 && j-1>=0 && i+1<n && j+1<n)
                b[i][j]=a[i][j]^a[i][j+1]^a[i+1][j+1]^a[i+1][j]^a[i+1][j-1]^a[i][j-1]^a[i-1][j-1];
            }      
        }
        for(i=0;i<n;i++)
            for(j=0;j<n;j++)
                a[i][j]=b[i][j];
        for(i=0;i<n;i++)
        {
            for(j=0;j<n;j++)
            {
                cout<<a[i][j]<<" ";
            }
            cout<<"\n";
        }
        no++;
    }
}