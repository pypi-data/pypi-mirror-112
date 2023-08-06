import matplotlib_inline
from numpy.core.fromnumeric import mean, shape
import pandas as pd
import numpy as np
df = pd.read_csv("C:\\Users\\Ankit\\OneDrive\\Documents\\Python\\OneWayAnova.csv", header = None)
print(df)


# first we've to compute the means for the values and store them
print(df.mean())
# storing the means in the variable mean
means = df.mean()
print(means)
#print (means[0])

k= df.columns   # prints the column in the df
print(k)

print(len(df.columns))  # trivial enough

#between groups
#SSB = (means[0]-means.means())*(means[0]-means.means()) # not a good way to do it, use iteration
#meanOfMeans  = means.mean()  # gives total mean, not a good way to do it, 
meanOfMeans = 0
k=len(df.columns)-1
n=len(df.columns)*len(df)
s=0
for i in range (len(df)):
    for j in range(len(df.columns)):
        s= s + df.loc[i,j]

meanOfMeans= s / n

#ANOVA USING FUNCTIONS 

# finds out n and k 
def get_n_k(df):
    n = len(df)
    k = len(df.columns)
    return n,k
#print(n)
print(n,k)

# Gets the means 
def getTreatmentMeans(df):
    return df.mean()
#print(df.mean)

def getTotalMean(df):
    x = np.array(df)
    x=x.reshape(40,1)
    return x.mean()

def getSSB(df, TreatmentMeans):
    if len(df.columns)!= len(TreatmentMeans):  # if df colums is not equal to length of treatement means then it can't be done 
        return "error"
    SSB = 0
    for i in range (len(TreatmentMeans)):
        SSB = SSB + (means[i] - meanOfMeans)**2
    return SSB*len(df)

def getSSW(df, TotalMean):
    SSW = 0
    for i in range (len(df.columns)):
        for j in range (len(df)):
            SSW = SSW + (df.loc[j,i] - means[i])**2
    return SSW

def ANOVA(df):
    n , k = get_n_k(df)
    TreatmentMeans = getTreatmentMeans(df)
    TotalMean = getTotalMean(df)
    SSB = getSSB(df, TreatmentMeans)
    SSW = getSSW(df, TotalMean)
    MSB = SSB/(k-1) 
    MSW = SSW/(n*k-k)
    return MSB/MSW
print("Your Reqired ANOVA is : -")
print(ANOVA(df))
print("Your Reqired TotalMean is : -")
print(getTotalMean(df))
print("Your Reqired TreatmentMeans is : -")
print(getTreatmentMeans(df))
print("Your Reqired SSB is : -")
print(getSSB(df,getTreatmentMeans(df)))
print("Your Reqired SSW is : -")
print(getSSW(df,getTotalMean(df)))

