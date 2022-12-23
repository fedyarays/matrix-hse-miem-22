import copy
import numpy


class Matrix:
    """
    Класс Matrix:
    1) Операторы: +(add), -(sub), *(mul), [n:m:](getitem) **-1(pow), ~(invert)
    2) Методы: транспонирование(trans), удаление строк(delete), перестановка строк(permutation),
     получение ранга(rang), получение размера(size), вывод матрицы(to_list)
     Ни одна функция не изменяет исходную матрицу, а возвращает новый объект.
    """

    def __init__(self, matrix: list):
        """
        Создание матрицы. Принимает массив как аргумент, создаёт объект класса Matrix,
        проверяет, является ли аргумент матрицей
         """
        for i in range(len(matrix) - 1):
            if len(matrix[i]) != len(matrix[i + 1]):
                raise ValueError("Несуществующая матрица")
        self.matrix = matrix

    def __add__(self, other):  # СЛОЖЕНИЕ
        """
        Осуществляет сложение двух матриц.
        :param other: вторая матрица.
        :return: новая матрица.
        """
        try:
            c = []  # Создаём пустой массив
            for i in range(len(self.to_list())):
                c.append(list(map(lambda x, y: x + y,
                                  self.to_list()[i],
                                  other.matrix[i])))  # Записываем в массив c сумму поэлементно
            return Matrix(c)
        except IndexError:  # Проверка на Index out of range
            raise IndexError("Матрицы разных размеров")

    def __sub__(self, other):  # ВЫЧИТАНИЕ
        """
        Осуществляет вычетание двух матриц.
        :param other: вторая матрица.
        :return: новая матрица.
        """
        try:
            c = []  # Создаём пустой массив
            for i in range(len(self.to_list())):
                c.append(list(map(lambda x, y: x - y,
                                  self.to_list()[i],
                                  other.matrix[i])))  # Записываем в массив c сумму поэлементно
            return Matrix(c)
        except IndexError:  # Проверка на Index out of range
            raise IndexError("Матрицы разных размеров")

    def __mul__(self, other):  # УМНОЖЕНИЕ
        """
        Осуществляет умножение матриц на число или матрицу.
        :param other: вторая матрица или число.
        :return: новая матрица.
        """
        if isinstance(other, int) or isinstance(other, float):  # Умножение на число
            matrix = copy.deepcopy(self.to_list())  # Создаём копию исходного массива
            for i in range(len(matrix)):
                matrix[i] = [x * other for x in matrix[i]]  # Записываем в копию массива произведение элемента и числа
            return Matrix(matrix)

        try:  # Умножение на матрицу
            size_matrix = len(self.to_list())
            c = [[] for _ in range(size_matrix)]  # Создаём пустой двумерный массив
            for i in range(size_matrix ** 2):
                t_matrix = other.trans().matrix  # Транспонируем матрицу
                c[i // size_matrix].append(
                    sum(list(map(  # Умножаем каждый элемент 1 матрицы на элемент 2 матрицы с тем же индексом
                        lambda x, y: x * y,
                        self.to_list()[i // size_matrix],
                        t_matrix[i % size_matrix]))))
            return Matrix(c)
        except IndexError:
            raise IndexError("Матрицы разных размеров")

    def __getitem__(self, val):  # ВЫВОД СТРОК
        """
        Осуществляет вывод элементов матрицы. Счет начинается с нуля. mat1[0:1:] - первая строка.
        Чтобы вывести столбцы, нужно транспонировать матрицу (mat.trans)
        mat1.trans()[0:1:] - первый столбец. Грубо говоря, выводятся с нулевой по первую строки.
        :param val: номер строки.
        :return: список.
        """
        if isinstance(val, slice):
            return self.matrix[val]
        else:
            raise TypeError("Индексы должны иметь вид [x:y:]")

    def __pow__(self, power=-1):  # ОБРАТНАЯ МАТРИЦА
        """
        Осуществляет нахождение обратной матрицы с помощью numpy.
        :param power: степень, в которую возводим матрицу (по умолчанию -1).
        :return: новая матрица.
        """
        if numpy.linalg.det(self.to_list()) == 0:
            raise ZeroDivisionError("Обратной матрицы не существует")
        try:
            err = 0
            m = self.to_list()
            np_inverted = numpy.linalg.inv(m)  # Нахождение обратной матрицы с помощью библиотеки numpy
            inv = numpy.stack(np_inverted).tolist()
            inverted = []
            k = 0
            for i in inv:
                inverted.append([])
                for j in i:
                    inverted[k].append(round(j, 5))
                k += 1
            return Matrix(inverted)
        except numpy.linalg.LinAlgError:
            raise ValueError("Матрица должна быть квадратной")

    def get_copy(self):  # КОПИЯ
        """
        Осуществляет создание копии матрицы.
        :return: новая матрица.
        """
        c = copy.deepcopy(self)
        return c

    def __invert__(self):  # ДЕТЕРМИНАНТ
        """
        Осуществляет нахождение определителя (детерминанта) матрицы.
        :return: число.
        """
        if len(self.to_list()) == len(self.to_list()[0]):  # Проверка матрицы на квадратность
            matrix = copy.deepcopy(self.to_list())
            count = 0
            if len(matrix) == 1:
                return matrix[0][0]
            else:
                for i in range(len(matrix)):
                    m = Matrix(matrix).delete("строка", 1)
                    m = m.delete("столбец", i+1)
                    count += matrix[0][i] * m.__invert__() * (-1) ** (
                                i + 2)  # Детерминант складывается из произведений по теореме Лапласа
            return count
        else:
            raise ValueError("Матрица должна быть квадратной")

    def trans(self):  # ТРАНСПОНИРОВАНИЕ
        """
        Осуществляет транспонирование матрицы.
        :return: новая матрица.
        """
        return Matrix(list(map(list, zip(*self.to_list()))))  # Сменить строки на столбцы

    def delete(self, type, number):  # УДАЛЕНИЕ
        """
        Осуществляет удаление строки или столбца матрицы.
        :param type: "строка" или "столбец"
        :param number: номер строки или столбца
        :return: новая матрица.
        """
        number -= 1
        matrix = copy.deepcopy(self.to_list())
        if type == "строка":
            del matrix[number]
        if type == "столбец":
            matrix = Matrix(matrix).trans().to_list()
            del matrix[number]
            matrix = Matrix(matrix).trans().to_list()
        return Matrix(matrix)

    def permutation(self, line_column: str, number_i, number_j):  # ПЕРЕСТАНОВКА
        """
        Осуществляет перестановку строк или столбцов матрицы.
        :param line_column: "строка" или "столбец"
        :param number_i: номер строки/столбца
        :param number_j: номер строки/столбца
        :return: новая матрица.
        """
        number_i -= 1
        number_j -= 1
        if line_column.lower() == "строка":  # Поменять местами две строки
            matrix = copy.deepcopy(self.to_list())
            matrix[number_i], matrix[number_j] = matrix[number_j], matrix[number_i]
        elif line_column.lower() == "столбец":  # Транспонировать и поменять местами две строки
            matrix = Matrix(self.to_list()).trans().matrix
            matrix[number_i], matrix[number_j] = matrix[number_j], matrix[number_i]
            matrix = Matrix(matrix).trans().matrix
        else:
            raise ValueError("Введите 'строка' или 'столбец'")
        return Matrix(matrix)

    def rang(self):  # РАНГ
        """
        Осуществляет нахождение ранга матрицы с помощью numpy.
        :return: число.
        """
        mat = self.to_list()
        return numpy.linalg.matrix_rank(mat)  # Нахождение ранга с помощью библиотеки numpy

    def size(self):  # РАЗМЕР
        """
        Осуществляет нахождение размера матрицы.
        :return: количество строк и количество столбцов.
        """
        return f"{len(self.to_list())} строк, {len(self.to_list()[0])} столбцов"

    def to_list(self):  # ВЫВОД МАТРИЦЫ
        """
        Осуществляет вывод матрицы.
        :return: лист(массив).
        """
        return self.matrix


# ПРИМЕР РАБОТЫ

if __name__ == "__main__":
    array1 = [[0, 1, 3, 4, 5, 6, 6],
              [2, 1, 7, 4, 5, 9, 6],
              [0, 1, 3, 10, 5, 6, 6],
              [15, 1, 3, 11, 5, 9, 5]]

    array2 = [[3, -5],
              [1, -2]]

    array3 = [[3, 3, 3, 3, 5, 6, 6],
              [2, 1, 7, 66, 5, 9, 6],
              [0, 1, 3, 70, 5, 6, 6],
              [15, 1, 23, 431, 5, 9, 5]]

    array4 = [[3, 3, 3, 3, 5, 6, 6],
              [0, 0, 7, 0, 5, 9, 6],
              [121, 1, 3, 70, 43, 897, 57676],
              [15, 1, 23, 431, 5, 9, 5]]

    mat1 = Matrix(array1)
    mat2 = Matrix(array2)
    mat3 = Matrix(array3)
    mat4 = Matrix(array4)

    mat_sum = mat1 + mat4
    mat_sum = mat1.__add__(mat4)

    mat_sub = mat1 - mat4
    mat_sub = mat1.__sub__(mat4)

    mat_mul = mat1 * mat3
    mat_mul = mat1.__mul__(mat3)
    mat_mul1 = mat2 * 10

    mat_elem = mat1[1:2:]

    mat_inv = mat2 ** -1
    mat_inv = mat2.__pow__(-1)

    mat_determinant = ~mat2

    mat_del = mat1.delete("строка", 1)

    mat_del_2 = mat1.delete("столбец", 1)

    """
    print("Матрица 1 + Матрица 4: ", mat_sum.to_list())
    print("Матрица 1 - Матрица 4: ", mat_sub.to_list())
    print("Матрица 1 * Матрица 4: ", mat_mul.to_list())
    print("Матрица 2 * 10: ", mat_mul1.to_list())
    print(mat1[0:1:])
    print("Обратная матрица 2:", (mat2**-1).to_list())
    print("Обратная матрица 2:", (mat2.__pow__().to_list()))
    print("Копия матрицы 2:", mat2.get_copy().to_list())
    print("Детерминант матрицы 2: ", ~mat2)
    print("Транспонированная матрица 3: ", mat3.trans().to_list())
    print("Удаление 1 строки матрицы 1: ", mat_del.to_list())
    print("Удаление 1 столбца матрицы 1: ", mat_del_2.to_list())
    print("Перестановка строк 1 и 2 матрицы 4: ", mat4.permutation("строка",1,2).to_list())
    print("Ранг матрицы 1:", mat1.rang())
    print("Размер матрицы 1:", mat1.size())
    print("Матрица 1: ", mat1.to_list())
    print(Matrix.__init__.__doc__)
    print(Matrix.to_list.__doc__)
    """

    print("Работа matrix.py завершена")








