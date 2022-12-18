import copy
import numpy

class Matrix:
    def __init__(self, matrix: list): # Принимает массив как аргумент
        self.matrix = matrix
        for i in range(len(matrix) - 1):
            if len(matrix[i]) != len(matrix[i + 1]): # Двумерный массив не является матрицей, если длины его элементов разные
                raise ValueError("Несуществующая матрица")

    def __add__(self, other): # Сложение матрицы
        try:
            c = [] # Создаём пустой массив
            for i in range(len(self.to_list())):
                c.append(list(map(lambda x, y: x + y,
                                  self.to_list()[i],
                                  other.matrix[i])))  # Записываем в массив c сумму поэлементно
            return Matrix(c)
        except IndexError:  # Проверка на Index out of range
            raise IndexError("Матрицы разных размеров")

    def __sub__(self, other): # Вычитание из матрицы
        try:
            c = [] # Создаём пустой массив
            for i in range(len(self.to_list())):
                c.append(list(map(lambda x, y: x - y,
                                  self.to_list()[i],
                                  other.matrix[i])))  # Записываем в массив c сумму поэлементно
            return Matrix(c)
        except IndexError:  # Проверка на Index out of range
            raise IndexError("Матрицы разных размеров")

    def __mul__(self, other): # Умножение матрицы
        if isinstance(other, int) or isinstance(other, float):  # Умножение на число
            matrix = copy.deepcopy(self.to_list()) # Создаём независимую копию исходного массива
            for i in range(len(matrix)):
                matrix[i] = [x * other for x in matrix[i]] # Записываем в копию массива произведение элемента и числа
            return Matrix(matrix)

        try: # Умножение на матрицу
            size_matrix = len(self.to_list())
            c = [[] for _ in range(size_matrix)] # Создаём пустой двумерный массив
            for i in range(size_matrix ** 2):
                t_matrix = other.trans().matrix  # Транспонируем матрицу, чтобы умножать строку на строку
                c[i // size_matrix].append(sum(list(map( # Умножаем каждый элемент 1 матрицы на элемент 2 матрицы с тем же индексом
                                 lambda x, y: x * y,
                                 self.to_list()[i // size_matrix],
                                 t_matrix[i % size_matrix]))))
            return Matrix(c)
        except IndexError:
            raise IndexError('Матрицы разных размеров')

    def __getitem__(self, val): # Вывод элемента матрицы
        if isinstance(val, slice):
            return self.matrix[val]

    def __pow__(self, power=-1): # Нахождение обратной матрицы
        if self.det() == 0:
            raise ZeroDivisionError("Обратной матрицы не существует")
        try:
            m = self.to_list()
            np_inverted = numpy.linalg.inv(m) # Нахождение обратной матрицы с помощью библиотеки numpy
            inverted = numpy.array(np_inverted)
            return Matrix(inverted)
        except numpy.linalg.LinAlgError:
            raise ValueError("Матрица должна быть квадратной")

    def get_copy(self): # Независимая копия матрицы
        c = copy.deepcopy(self)
        return c

    def det(self): # Детерминант матрицы
        matrix = copy.deepcopy(self.to_list())
        count = 0
        if len(matrix) == 1:
            return matrix[0][0]
        else:
            for i in range(len(matrix)):
                m = Matrix(matrix).delete(1, i + 1)
                count += matrix[0][i] * m.det() * (-1) ** (i + 2) # Детерминант складывается из произведений по теореме Лапласа
        return count

    def trans(self): # Транспонирование матрицы
        return Matrix(list(map(list, zip(*self.to_list())))) # Сменить строки на столбцы

    def delete(self, line, column): # Удаление строки и столбца матрицы
        line -= 1
        column -= 1
        matrix = copy.deepcopy(self.to_list())
        del matrix[line] # Удаление строки
        for item in range(len(matrix)): # Удаление столбца
            del matrix[item][column]
        return Matrix(matrix)

    def permutation(self, line_column: str, number_i, number_j): # Перестановка строк или столбцов матрицы
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

    def rang(self): # Нахождение ранга матрицы
        mat = self.to_list()
        return numpy.linalg.matrix_rank(mat) # Нахождение ранга с помощью библиотеки numpy

    def size(self): # Нахождение размера матрицы
        return f"{len(self.to_list())} строк, {len(self.to_list()[0])} столбцов"

    def to_matrix(self): # Вывод матрицы в форме двумерного массива
        return self.matrix

# ПРИМЕР РАБОТЫ

array1 = [[0, 1, 3, 4, 5, 6, 6],
          [2, 1, 7, 4, 5, 9, 6],
          [0, 1, 3, 10, 5, 6, 6],
          [15, 1, 3, 11, 5, 9, 5]]

array2 = [[3, -5],
          [1, -2],]


mat1 = Matrix(array1)
mat2 = Matrix(array2)
mat_sum = mat1 + mat1

print(mat1.to_list())
print(mat_sum.to_list())
print(mat1.rang())
print((mat2**-1).to_list())
print(mat1[1:2:])