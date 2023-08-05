"""
    Functions within this module allow for the use of multiple test statistics
    that can be used for independent p values. Combined p value output functionality is also added
    Method options include: Fisher, Pearson, Ed, Stouffer, George, Tippett
"""

#Purpose: Combining P-values methodology
#Author: Breya McGlown
#Math Master's Thesis

__version__ = "0.1.4"

import numpy as np
import copy
from scipy.stats import norm
import math as mt
from scipy.stats import t
from scipy.stats import chi2
from scipy.stats import gamma
from scipy.stats import beta

class CountPs:
    """
    Functions within this module allow for the use of multiple test statistics
    that can be used for independent p values. Combined p value output functionality is also added
    Method options include: Fisher, Pearson, Ed, Stouffer, George, Tippett
    """

    def __init__(self, method):
        self.method = method

    def SumOfPs(self, *args):
        """
        Select n number of p-values to use with desired method
        enter p values into args parameter
        """
        if self.method == self.method:
            self.N = list(args)
            pass
        return list(args)

    def FisherMethod(self,output):
        """
        Fishers method
        """
        if self.method == 'Fisher':
            self.output = output
            List = output
            temp = []
            for x in List:
                temp.append(mt.log(x))
            temp1 = -2* sum(temp)
            output = temp1 #-2SF is distributed chisquare 2 ddof

        return output

    def PearsonMethod(self,output):
        """
        Pearsons Method
        """
        if self.method == 'Pearson':
                self.output = output
                List = output
                temp = []
                for x in List:
                    temp.append(mt.log(1 - x))
                temp1 = -2* sum(temp)
                output = temp1 #-2SP is distributed chisquare 2 ddof

        return output

    def GeorgeMethod(self,output):
        """
        Georges Method
        """
        if self.method == 'George':
                self.output = output
                List = output
                temp = []
                for x in List:
                    temp.append(mt.log(x/(1 - x)))
                temp1 = -1 * sum(temp) #SF-SP
                output = temp1 #SG is distributed t distribution

        return output

    def EdMethod (self,output):
        """
        Edgington's Method
        """

        if self.method == 'Ed':
            self.output = output
            List = output
            temp = []
            for x in List:
                temp.append(x)
            temp1 = sum(temp)
            output = temp1 #SE is Gaussian Distribution

        return output

    def StoufferMethod(self,output):
        """
        StoufferMethod
        """

        if self.method == 'Stouffer':
            self.output = output
            List = output
            temp = []
            for x in List:
                temp.append(norm.ppf(x)) #inverse CDF
            temp1 = sum(temp)
            output = temp1 #SS is N(0,n)

        return output

    def TippettMethod(self,output):
        """
        Tippett Method
        """
        if self.method == 'Tippett':
            self.output = output
            List = output
            output = min(List) #ST is Beta(1,n)

        return output

    def CombinedPvalue(self,output):
        """
        Returns the p value of the combined pvalues based on the 
        method selected
        """
        self.n = len(self.N)

        if self.method == 'Tippett':
            self.output = output
            output = 1-(1-output)**self.n#beta.pdf(output,a = 1, b = self.n) #ST is Beta(1,n)
        elif self.method == 'Stouffer':
            self.output = output
            output = norm.pdf(output,scale = self.n) #SS is N(0,n)
        elif self.method == 'George':
            self.output = output
            output = t.pdf(output,self.n) #SG is Student t distribution (n)
        elif self.method == 'Ed':
            self.output = output
            output = gamma.pdf(output,a = self.n) #SE is Gamma(x,n)
        elif self.method == 'Pearson':
            self.output = output
            output = chi2.cdf(output,2*self.n) #SP is Chi-square df=2n
        else:
            self.output = output
            output = chi2.pdf(output,2*self.n) #SF is Chi-square df=2n
        
        return output


if __name__ == "__main__":
 
    A = CountPs('Tippett') #Fisher, Pearson, Ed, Stouffer, George, Tippett
    Output = A.SumOfPs(0.1,.3,.7)
    Final = A.TippettMethod(Output)
    SignOrNot = A.CombinedPvalue(Final)
    #print(Final, SignOrNot)

    #Test
    #random generator 10,12,15,18,20 N(mu,sigma^2) various values of mu and sigma^2
    mu = np.random.random_integers(low = 1,high = 10, size = 1)
    sigma = np.random.random_integers(low = 0,high = 10, size = 1)
    List = [10,12,15,18,20] #sample size
    PvalsFromPaper = [0.585,0.76,0.365,0.905,0.08,0.265,0.405,0.76,0.1,0.25,0.185,0.115,0.525,0.035,0.65,0.035,0.075,0.01,0.205,0.43,0.52,0.435,0.12]
    for x in List:
        Various = np.random.normal(mu, sigma, x)
        Pvalues = norm.cdf(Various)
        Output = A.SumOfPs(Pvalues)
        #Get P values and combine
        Final = A.StoufferMethod(Output[0])
        #print(Final)
        SignOrNot = A.CombinedPvalue(Final)

    #Get P values and Combine

    #random generator 10,12,15,18,20 t-statistic N(0,sigma^2)
    #Based on t-statistic each sample to test mu = 0. get P values and combine
    #mu = 0
    #sigma = np.random.random_integers(low = 1,high = 10, size = 1)
    List = [10,12,15,18,20] #sample size
    for x in List:
        Various = t.rvs(x-1, size = x)
        Pvalues = t.cdf(Various,x-1)
        Output = A.SumOfPs(Pvalues)
        #Get P values and combine
        Final = A.StoufferMethod(Output[0])
        #print(Final)
        SignOrNot = A.CombinedPvalue(Final)

    #Testing functionality based on P values provided by Cheng and Sheng paper
    
    Test = A.SumOfPs(PvalsFromPaper)
    print(Test)
    #Stouffer's test
    A = CountPs('Stouffer')
    StouffersOut = A.StoufferMethod(copy.deepcopy(Test[0]))
    #print(StouffersOut)
    
    
    #Fishers Test against metap_beckerp.csv data used in R tests
    A = CountPs('Tippett')
    Input = A.SumOfPs(0.016,0.067,0.25,0.405,0.871)
    TippettOut = A.TippettMethod(Input)
    SignOrNot = A.CombinedPvalue(TippettOut)
    print(TippettOut, SignOrNot)


    

    


