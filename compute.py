import numpy as np
import pandas as pd


class Compute():

    def dropped_nodes(self,numero):
        lista = (pd.read_csv(f'experimentation/dropped_nodes/dropped_nodes_{numero}.csv',header = None)).iloc[:,0].values.tolist()
        return np.array(lista,dtype = np.int32)

    def calculate_time(self, matrix, numero):
        ''' Calculate the time matrix for the time n'''

        lista = self.dropped_nodes((numero-1))
        time_1 = pd.read_csv('experimentation/time_matrix/time_matrix_day1.csv',header = None)

        #4 beacuse they are deprived with 1 day per different distribution
        matrix.iloc[:,lista] = (matrix.iloc[:,lista] + 12)
        matrix.iloc[lista,:] = (matrix.iloc[lista,:] + 12)
        matrix.loc[~matrix.index.isin(lista),:] = time_1.loc[~matrix.index.isin(lista),:]
        matrix.loc[:,~matrix.index.isin(lista)] = time_1.loc[:,~matrix.index.isin(lista)]

        matrix = np.array(matrix)
        np.fill_diagonal(matrix,0)

        #That is the time_matrix for the time n (not necesarilly n)
        np.savetxt(f'experimentation/time_matrix/time_matrix_day{numero}.csv',matrix,delimiter=",")


    def recompute(self,numero):
        matrix = pd.read_csv(f'experimentation/time_matrix/time_matrix_day{numero-1}.csv',header = None)
        self.calculate_time(matrix,numero)

        time_matrix = pd.read_csv(f'experimentation/time_matrix/time_matrix_day{numero}.csv',header = None)

        deprivation_cost = np.exp(1.5031 + 0.1172*time_matrix) + np.exp(1.5031)


        deprivation_cost = np.array(deprivation_cost)
        np.fill_diagonal(deprivation_cost,0)
        np.savetxt(f'experimentation/dep_costs/dep_cost_day{numero}.csv',deprivation_cost,delimiter=",")
