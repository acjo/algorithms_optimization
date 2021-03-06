"""Volume 2: Simplex

Caelan Osman
Math 323 Sec. 2
March 3, 2021
"""

import numpy as np


# Problems 1-6
class SimplexSolver(object):
    """Class for solving the standard linear optimization problem

                        minimize        c^Tx
                        subject to      Ax <= b
                                         x >= 0
    via the Simplex algorithm.
    """
    # Problem 1
    def __init__(self, c, A, b):
        """Check for feasibility and initialize the dictionary.

        Parameters:
            c ((n,) ndarray): The coefficients of the objective function.
            A ((m,n) ndarray): The constraint coefficients matrix.
            b ((m,) ndarray): The constraint vector.

        Raises:
            ValueError: if the given system is infeasible at the origin.
        """
        #checking feasibility at the origin
        if np.any(b < 0):
            raise ValueError('Problem Infeasible at the origin')

        #generate dictionary
        self._generatedictionary(c, A, b)

    # Problem 2
    def _generatedictionary(self, c, A, b):
        """Generate the initial dictionary.

        Parameters:
            c ((n,) ndarray): The coefficients of the objective function.
            A ((m,n) ndarray): The constraint coefficients matrix.
            b ((m,) ndarray): The constraint vector.
        """

        c = np.concatenate((np.zeros(1), c, np.zeros(A.shape[0])))
        A = np.hstack((A, np.eye(A.shape[0])))
        D = np.column_stack((b, -A))
        D = np.vstack([c, D])

        self.D = D

    # Problem 3a
    def _pivot_col(self):
        """Return the column index of the next pivot column.
        """
        #get mask
        mask = self.D[0, 1:] < 0

        #check that at least one coefficient is negative
        if not np.any(mask):
            raise ValueError('No coefficient is negative')

        #return column index that whose element is less than zero (smallest index -> bland's rule)
        column_index = np.argmax(mask) + 1
        return column_index


    # Problem 3b
    def _pivot_row(self, index):
        """Determine the row index of the next pivot row using the ratio test
        (Bland's Rule).
        """

        #get pivot column
        column = self.D[1:, index]
        #get elements less than zero
        mask = column < 0
        #check feasibility
        if not np.any(mask):
            raise ValueError('Problem is unbounded')

        #get dictionary of ratios mapping to index
        #adding back one to account for the loss of the first element
        #go backwards to replace any duplicates with a smaller index (bland's rule)
        ratios = {-self.D[i + 1, 0] / column[i] : i + 1 for i in range(mask.size-1, -1, -1) if mask[i]}
        #get minimum row index
        row_index = ratios[min(ratios)]
        return row_index

    # Problem 4
    def pivot(self):
        """Select the column and row to pivot on. Reduce the column to a
        negative elementary vector.
        """
        #get pivot column and row indexes
        col = self._pivot_col()
        row = self._pivot_row(col)

        #divide pivot row
        self.D[row, :] /= -self.D[row, col]

        #zero out rows above and below
        for i in range(self.D.shape[0]):
            if i == row:
                continue
            #element in the pivot column of the current row
            pivot_element = self.D[i, col]
            self.D[i, :] += (pivot_element * self.D[row, :])


    # Problem 5
    def solve(self):
        """Solve the linear optimization problem.

        Returns:
            (float) The minimum value of the objective function.
            (dict): The basic variables and their values.
            (dict): The nonbasic variables and their values.
        """

        #run pivoting until a value error occurs
        try :
            while True:
                self.pivot()
        except ValueError:
            #find optimal value
            optimal = self.D[0, 0]
            #set up empty dictionaries
            basic = {}
            non_basic = {}
            #create new mask to identify independent and dependent variables
            mask = abs(self.D[0, :]) < 1e-10

            #run through all columns and mask values
            for col, truth in enumerate(mask):
                #skip the first column
                if col == 0:
                    continue
                #if a 1st row column element is zero
                elif truth:
                    #get nonzero values
                    nonzero = self.D[1:, col] != 0
                    #get row index (plus one for ignoring first row)
                    row_index = np.argmax(nonzero) + 1
                    #dependent variable values.
                    basic[col - 1] = self.D[row_index, 0]

                #set independent variable values to 0.
                else:
                    non_basic[col-1] = 0

            return optimal, basic, non_basic

# Problem 6
def prob6(filename='productMix.npz'):
    """Solve the product mix problem for the data in 'productMix.npz'.

    Parameters:
        filename (str): the path to the data file.

    Returns:
        ((n,) ndarray): the number of units that should be produced for each product.
    """
    data = np.load(filename)

    #extract data
    A = data['A']
    p = data['p']
    m = data['m']
    d = data['d']

    b = np.concatenate((m, d))
    m = p.size

    I = np.eye(d.size)
    #create new A matrix encapsulating all constraint values
    A = np.vstack((A, I))
    #create new boundrie array

    #solve simplex method (negating p) to turn into a min problem
    simplex = SimplexSolver(-p, A, b)
    solution = simplex.solve()

    #alternate way to define
    #units_1 = np.array([solution[1][i] if i in solution[1] else 0 for i in range(m)])

    #combine solution dictionaries
    x = {**solution[1], **solution[2]}
    #return the values of the m original variables
    units = np.array([x[i] for i in range(m)])
    return units


if __name__ == "__main__":

    #problem 1
    '''
    c = np.array([-3, -2])
    b = np.array([2, -5, 7])
    A = np.array([[1, -1], [3, 1], [4, 3]])
    simplex = SimplexSolver(c, A, b)
    '''

    #problem 2
    '''
    c = np.array([-3, -2])
    b = np.array([2, 5, 7])
    A = np.array([[1, -1], [3, 1], [4, 3]])
    simplex = SimplexSolver(c, A, b)
    D_actual = np.array([[0, -3, -2, 0, 0, 0], [2, -1, 1, -1, 0, 0],
                         [5, -3, -1, 0, -1, 0], [7, -4, -3, 0, 0, -1]])

    print(np.allclose(simplex.D, D_actual))

    '''

    #problem 3 and 4
    '''
    c = np.array([-3, -2])
    b = np.array([2, 5, 7])
    A = np.array([[1, -1], [3, 1], [4, 3]])
    simplex = SimplexSolver(c, A, b)
    simplex.pivot()
    D_actual = np.array([[-5, 0, -1, 0, 1, 0], [1/3., 0, 4/3., -1, 1/3., 0],
                         [5/3., -1, -1/3., 0, -1/3., 0], [1/3, 0, -5/3, 0, 4/3., -1]])
    print(np.allclose(simplex.D, D_actual))
    '''


    #problem 5
    '''
    c = np.array([-3, -2])
    b = np.array([2, 5, 7])
    A = np.array([[1, -1], [3, 1], [4, 3]])
    simplex = SimplexSolver(c, A, b)
    sol = simplex.solve()

    D_actual = np.array([[-5.2, 0, 0, 0, 0.2, 0.6], [0.6, 0, 0, -1, 1.4, -0.8],
                         [1.6, -1, 0, 0, -0.6, 0.2], [0.2, 0, -1, 0, 0.8, -0.6]])

    print(np.allclose(simplex.D, D_actual))
    print(sol)
    '''

    #problem 6
    #print(prob6())
