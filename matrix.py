import random
import math

class matrix():

    def adding_numbers(self):
        for i in range(self.rows):
            self.data.append([])
            for n in range(self.cols):
                self.data[i].append(random.uniform(-1,1))

    def __init__(self,rows,cols):
        self.rows = rows
        self.cols = cols
        self.data = []
        self.adding_numbers()

    def copy_matrix(self,m1):
        for i in range(self.rows):
            for n in range(self.cols):
                self.data[i][n] = m1[i][n]

    def new_weights(self,n_in):
        value = 1 / math.sqrt(n_in)
        for i in range(self.rows):
            for n in range(self.cols):
                self.data[i][n] = random.uniform(-value,value)

    def multiply_static(m1,m2):
        if m2.rows != m1.cols:
            print ('operacije nije moguca')
        else:
            new_matrix = matrix(m1.rows,m2.cols)
            for n in range(new_matrix.rows):
                for m in range(new_matrix.cols):
                    suma = 0
                    for i in range(m1.cols):
                        suma += m1.data[n][i] * m2.data[i][m]
                    new_matrix.data[n][m] = suma
            return new_matrix

    def multyply_scalar(self,p):
            for i in range(self.rows):
                for n in range(self.cols):
                    self.data[i][n] *= p

    def multyply_matrix(self,m1):
            for i in range(self.rows):
                for n in range(self.cols):
                    self.data[i][n] *= m1.data[i][n]

    def transpose_static(m1):
        result = matrix(m1.cols,m1.rows)
        for j in range(result.rows):
            for i in range(result.cols):
                result.data[j][i] = m1.data[i][j]
        return result

    def add(self,p):
        if isinstance(p, matrix):
            for i in range(self.rows):
                for n in range(self.cols):
                    self.data[i][n]  += p.data[i][n]
        else:
            for i in range(self.rows):
                for n in range(self.cols):
                    self.data[i][n] += p
        return  self.data

    def map(self,func):
        for i in range(self.rows):
             for n in range(self.cols):
                 val = self.data[i][n]
                 self.data[i][n] = func(val)

    def map_static(m1,func):
        result = matrix(m1.rows,m1.cols)
        for i in range(m1.rows):
                for n in range(m1.cols):
                    val = m1.data[i][n]
                    result.data[i][n] = func(val)
        return  result

    def fromArray(arr):
        m = matrix(len(arr),1)
        for i in range(len(arr)):
            m.data[i][0] = arr[i]
        return m

    def toArray(self):
        arr = []
        for i in range(self.rows):
            for j in range(self.cols):
                arr.append(self.data[i][j])
        return arr

    def subtract_static(a,b):
        result = matrix(a.rows,a.cols)
        if isinstance(a, matrix) and isinstance(b, matrix):
            for i in range(a.rows):
                for n in range(a.cols):
                    result.data[i][n] = a.data[i][n] - b.data[i][n]
        else:
            for i in range(a.rows):
                for n in range(a.cols):
                    result.data[i][n] = a.data[i][n] - b
        return  result



#arr = [1,2,3,4]

#c = matrix.fromArray(arr)

#print (c.data)
#print ('matrix 1:',var.data)
#print ('')
#print ('matrix 2:',var2.data)
#print ('')


#c = matrix.multyply_matrix(var,var2)
#print ('matrix 3:',var.data)
