import numpy as np
import pandas as pd


class Compute():

    def dropped_nodes(self,numero):
        lista = (pd.read_csv(f'experimentation/dropped_nodes/dropped_nodes_{numero}.csv',header = None)).iloc[:,0].values.tolist()
        return np.array(lista,dtype = np.int32)

    def calculate_time(matrix):
        time_1 = pd.read_csv('experimentation/time_matrix/time_matrix_day1.csv',header = None)

        matrix.iloc[:,lista] = (matrix.iloc[:,lista] + 4)
        matrix.iloc[lista,:] = (matrix.iloc[lista,:] + 4)
        matrix.loc[~matrix.index.isin(lista),:] = time_1.loc[~matrix.index.isin(lista),:]
        matrix.loc[:,~matrix.index.isin(lista)] = time_1.loc[:,~matrix.index.isin(lista)]

        matrix = np.array(matrix)
        np.fill_diagonal(matrix,0)

        matrix.iloc[lista,:]

    def recompute(self,numero):
        lista = self.dropped_nodes((numero-1))

        matrix = pd.read_csv(f'experimentation/time_matrix/time_matrix_day{numero-1}.csv',header = None)

        lista
        matrix
        """FIRST, WE HAVE TO SAVE THE NEW TIME MATRIX,
        DONT COMPUTE YET THE DEPRIVATION dep_costs"""



        # matrix.iloc[:,lista] = np.exp(1.50031 + 0.1172*(matrix.iloc[:,lista] + 8)) + np.exp(1.5031)
        # matrix.iloc[lista,:] = np.exp(1.50031 + 0.1172*(matrix.iloc[lista,:] + 8)) + np.exp(1.5031)
        # matrix.loc[~matrix.index.isin(lista),:] = dep_cost_1.loc[~matrix.index.isin(lista),:]
        # matrix.loc[:,~matrix.index.isin(lista)] = dep_cost_1.loc[:,~matrix.index.isin(lista)]

        matrix = np.array(matrix)
        np.fill_diagonal(matrix,0)

        return matrix




# np.exp(1.5031 + 0.1172*matrix) + np.exp(1.5031)
