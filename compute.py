import numpy as np
import pandas as pd


class Compute():

    def dropped_nodes(self,numero):
        lista = (pd.read_csv(f'experimentation/dropped_nodes/dropped_nodes_{numero}.csv',header = None)).iloc[:,0].values.tolist()
        return np.array(lista,dtype = np.int32)


    def recompute(self,numero):
        lista = self.dropped_nodes(numero)
        dep_cost_1 = pd.read_csv('experimentation/dep_costs/dep_cost_day1.csv',header = None)

        matrix = pd.read_csv('experimentation/time_matrix_day1.csv',header = None)
        matrix = matrix/3600

        matrix.iloc[:,lista] = np.exp(1.50031 + 0.1172*(matrix.iloc[:,lista] + 8)) + np.exp(1.5031)
        matrix.iloc[lista,:] = np.exp(1.50031 + 0.1172*(matrix.iloc[lista,:] + 8)) + np.exp(1.5031)
        matrix.loc[~matrix.index.isin(lista),:] = dep_cost_1.loc[~matrix.index.isin(lista),:]
        matrix.loc[:,~matrix.index.isin(lista)] = dep_cost_1.loc[:,~matrix.index.isin(lista)]


        matrix = np.array(matrix)
        np.fill_diagonal(matrix,0)

        return matrix




# np.exp(1.5031 + 0.1172*matrix) + np.exp(1.5031)
