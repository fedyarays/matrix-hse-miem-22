import copy
import numpy

class Matrix:
    def __init__(self, matrix: list):
        "Принимает массив как аргумент"
        for i in range(len(matrix) - 1):
            if len(matrix[i]) != len(matrix[i + 1]): # Двумерный массив не является матрицей, если длины его элементов разные
                raise ValueError("Несуществующая матрица")
        self.matrix = matrix

    def __add__(self, other):
        "Осуществляет сложение матриц. Возвращает матрицу"
        try:
            c = [] # Создаём пустой массив
            for i in range(len(self.to_list())):
                c.append(list(map(lambda x, y: x + y,
                                  self.to_list()[i],
                                  other.matrix[i])))  # Записываем в массив c сумму поэлементно
            return Matrix(c)
        except IndexError:  # Проверка на Index out of range
            raise IndexError("Матрицы разных размеров")

    def __sub__(self, other):
        "Осуществляет вычетание матриц. Возвращает матрицу"
        try:
            c = [] # Создаём пустой массив
            for i in range(len(self.to_list())):
                c.append(list(map(lambda x, y: x - y,
                                  self.to_list()[i],
                                  other.matrix[i])))  # Записываем в массив c сумму поэлементно
            return Matrix(c)
        except IndexError:  # Проверка на Index out of range
            raise IndexError("Матрицы разных размеров")

    def __mul__(self, other):
        "Осуществляет умножение матриц на число или матрицу. Возвращает матрицу"
        if isinstance(other, int) or isinstance(other, float):  # Умножение на число
            matrix = copy.deepcopy(self.to_list()) # Создаём копию исходного массива
            for i in range(len(matrix)):
                matrix[i] = [x * other for x in matrix[i]] # Записываем в копию массива произведение элемента и числа
            return Matrix(matrix)

        try: # Умножение на матрицу
            size_matrix = len(self.to_list())
            c = [[] for _ in range(size_matrix)] # Создаём пустой двумерный массив
            for i in range(size_matrix ** 2):
                t_matrix = other.trans().matrix  # Транспонируем матрицу
                c[i // size_matrix].append(sum(list(map( # Умножаем каждый элемент 1 матрицы на элемент 2 матрицы с тем же индексом
                                 lambda x, y: x * y,
                                 self.to_list()[i // size_matrix],
                                 t_matrix[i % size_matrix]))))
            return Matrix(c)
        except IndexError:
            raise IndexError("Матрицы разных размеров")

    def __getitem__(self, val):
        "Осуществляет вывод элементов матрицы. Выводит строки матрицы"
        if isinstance(val, slice):
            return self.matrix[val]
        else:
            raise TypeError("Индексы должны иметь вид [x:y:]")

    def __pow__(self, power=-1):
        "Осуществляет нахождение обратной матрицы. Возвращает матрицу"
        if self.__invert__() == 0:
            raise ZeroDivisionError("Обратной матрицы не существует")
        try:
            m = self.to_list()
            np_inverted = numpy.linalg.inv(m) # Нахождение обратной матрицы с помощью библиотеки numpy
            inverted = numpy.stack(np_inverted).reshape(len(m), len(m))
            return Matrix(inverted)
        except numpy.linalg.LinAlgError:
            raise ValueError("Матрица должна быть квадратной")

    def get_copy(self):
        "Осуществляет создание копии матрицы. Возвращает матрицу"
        c = copy.deepcopy(self)
        return c

    def __invert__(self):
        "Осуществляет определителя (детерминанта) матрицы. Возвращает число"
        if len(self.to_list()) == len(self.to_list()[0]): # Проверка матрицы на квадратность
            matrix = copy.deepcopy(self.to_list())
            count = 0
            if len(matrix) == 1:
                return matrix[0][0]
            else:
                for i in range(len(matrix)):
                    m = Matrix(matrix).delete(1, i + 1)
                    count += matrix[0][i] * m.__invert__() * (-1) ** (i + 2) # Детерминант складывается из произведений по теореме Лапласа
            return count
        else:
            raise ValueError("Матрица должна быть квадратной")

    def trans(self):
        "Осуществляет транспонирование матрицы. Возвращает матрицу"
        return Matrix(list(map(list, zip(*self.to_list())))) # Сменить строки на столбцы

    def delete(self, line, column):
        "Осуществляет удаление строки или столбца матрицы. Возвращает матрицу"
        line -= 1
        column -= 1
        matrix = copy.deepcopy(self.to_list())
        del matrix[line] # Удаление строки
        for item in range(len(matrix)): # Удаление столбца
            del matrix[item][column]
        return Matrix(matrix)

    def permutation(self, line_column: str, number_i, number_j):
        "Осуществляет перестановку строк или столбцов матрицы. Возвращает матрицу"
        number_i -= 1
        number_j -= 1
        if line_column.lower() == "строка": # Поменять местами две строки
            matrix = copy.deepcopy(self.to_list())
            matrix[number_i], matrix[number_j] = matrix[number_j], matrix[number_i]
        elif line_column.lower() == "столбец": # Транспонировать и поменять местами две строки
            matrix = Matrix(self.to_list()).trans().matrix
            matrix[number_i], matrix[number_j] = matrix[number_j], matrix[number_i]
            matrix = Matrix(matrix).trans().matrix
        else:
            raise ValueError("Введите 'строка' или 'столбец'")
        return Matrix(matrix)

    def rang(self):
        "Осуществляет нахождение ранга матрицы. Возвращает число"
        mat = self.to_list()
        return numpy.linalg.matrix_rank(mat) # Нахождение ранга с помощью библиотеки numpy

    def size(self): # Нахождение размера матрицы
        "Осуществляет нахождение размера матрицы. Возвращает число"
        return f"{len(self.to_list())} строк, {len(self.to_list()[0])} столбцов"

    def to_list(self):
        "Осуществляет вывод матрицы. Возвращает массив"
        return self.matrix

# ПРИМЕР РАБОТЫ

array1 = [[0, 1, 3, 4, 5, 6, 6],
          [2, 1, 7, 4, 5, 9, 6],
          [0, 1, 3, 10, 5, 6, 6],
          [15, 1, 3, 11, 5, 9, 5]]

array2 = [[3, -5],
          [1, -2],]

array3 = [[3, 3, 3, 3, 5, 6, 6],
          [2, 1, 7, 66, 5, 9, 6],
          [0, 1, 3, 70, 5, 6, 6],
          [15, 1, 23, 431, 5, 9, 5]]

array4 = [[3, 3, 3, 3, 5, 6, 6],
          [0, 0, 7, 0, 5, 9, 6],
          [121, 1, 3, 70, 43, 897, 57676],
          [15, 1, 23, 431, 5, 9, 5]]

mat1 = Matrix(array1)  # Объект класса Matrix (матрица 1)
mat2 = Matrix(array2)  # Объект класса Matrix (матрица 2)
mat3 = Matrix(array3)  # Объект класса Matrix (матрица 3)
mat4 = Matrix(array4)  # Объект класса Matrix (матрица 4)

mat_sum = mat1 + mat4
mat_sum = mat1.__add__(mat4)

mat_sub = mat1 - mat4
mat_sub = mat1.__sub__(mat4)

mat_mul = mat1 * mat3
mat_mul = mat1.__mul__(mat3)

mat_elem = mat1[1:2:]

mat_inv = mat2 ** -1
mat_inv = mat2.__pow__(-1)
"""
print(mat1.to_list())
print(mat_sum.to_list())
print(mat1.rang())
print((mat2**-1).to_list())
print(mat1[1:2:])
print(Matrix.__init__.__doc__)
print(Matrix.to_list.__doc__)
"""
