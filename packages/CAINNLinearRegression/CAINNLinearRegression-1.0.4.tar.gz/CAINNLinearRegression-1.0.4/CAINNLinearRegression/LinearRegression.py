
class LinearRegression():

    def __init__(self,X,Y):
        """
        init: (Features, Targets) 
        """
        self.x_inputs = X
        self.y_outputs = Y 
        self.number_of_elements = len(Y)
        self.m_a = 0
        self.m_b = 0

        self.error = 0
        self.a_gradient = 0
        self.b_gradient = 0

        self.convergence_itr = 0
        self.convergence_tracker = 0

    def train(self):
        """
        Once object is initilized with X and Y values, 
        call this method to fit the regression line 
        """

        while self.isConverged() == False :

            learning_rate = 0.001 
            self.a_gradient = 0
            self.b_gradient = 0

            for i, x_input in enumerate(self.x_inputs):
                self.a_gradient += x_input * ((self.m_a * x_input + self.m_b) - self.y_outputs[i])
            self.a_gradient = (2 * self.a_gradient) / self.number_of_elements

            for i, y_output in enumerate(self.y_outputs):
                self.b_gradient += ((self.m_a * self.x_inputs[i] + self.m_b) - y_output)
            self.b_gradient = (2 * self.b_gradient) / self.number_of_elements

            self.m_a = self.m_a - (self.a_gradient * learning_rate)
            self.m_b = self.m_b - (self.b_gradient * learning_rate)

    def isConverged(self):
        '''
        Check to see if the algorithm has converged on a optimum solution given its parameters.
        If so, this method will return True, otherwise it will return False. 
        Convergence considers the last ten times it was called to inform on decision.
        '''
        self.convergence_itr += 1
        total_gradient = (abs(self.a_gradient) + abs(self.b_gradient))
        if self.convergence_itr < 1000:
            self.convergence_tracker =  (self.convergence_tracker + total_gradient) / self.convergence_itr
            return False
        elif self.convergence_itr > 50000:
            #print("previous gradient: {}".format(self.convergence_tracker))
            #print("Converged after {} iterations".format(self.convergence_itr))
            return True
        
        if self.convergence_tracker  < 0.001:
           # print("total gradient: {}, previous gradient: {}".format(total_gradient, self.convergence_tracker))
            #print("Converged after {} iterations".format(self.convergence_itr))
            return True
        else:
            self.convergence_tracker = (self.convergence_tracker + total_gradient) / self.convergence_itr
            return False

    def regress(self, X):
        return self.m_a * X + self.m_b

    
"""
lr = LinearRegression([1,2,3,4,5], [2,4,6,8,10])
lr.train()
print(lr.regress(8))
"""

"""
import pandas as pd
path = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DA0101EN-SkillsNetwork/labs/Data%20files/automobileEDA.csv'
df = pd.read_csv(path)
X = df['highway-mpg']
Y = df['price']
lr = LinearRegression(X,Y)
lr.train()
print(lr.regress(X[0]))
print(lr.m_a)
print(lr.m_b)
"""
