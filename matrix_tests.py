from matrix import Matrix
from pytest import *
import numpy

array1 = [[0, 1, 3, 4, 5, 6, 6],
          [2, 1, 7, 4, 5, 9, 6],
          [0, 1, 3, 10, 5, 6, 6],
          [15, 1, 3, 11, 5, 9, 5]]

array2 = [[3, -5],
          [1, -2], ]

array3 = [[3, 3, 3, 3, 5, 6, 6],
          [2, 1, 7, 66, 5, 9, 6],
          [0, 1, 3, 70, 5, 6, 6],
          [15, 1, 23, 431, 5, 9, 5]]

array4 = [[3, 3, 3, 3, 5, 6, 6],
          [0, 0, 7, 0, 5, 9, 6],
          [121, 1, 3, 70, 43, 897, 57676],
          [15, 1, 23, 431, 5, 9, 5]]

m1 = Matrix(array1)
m2 = Matrix(array2)
m3 = Matrix(array3)
m4 = Matrix(array4)


def test_add():
    """
    Осуществляет проверку сложения двух матриц (работы функции add).
    :return: "Add test complete".
    """
    assert (m1 + m3).to_list() == [[3, 4, 6, 7, 10, 12, 12], [4, 2, 14, 70, 10, 18, 12], [0, 2, 6, 80, 10, 12, 12],
                                   [30, 2, 26, 442, 10, 18, 10]]
    assert (m1 + m4).to_list() == [[3, 4, 6, 7, 10, 12, 12], [2, 1, 14, 4, 10, 18, 12], [121, 2, 6, 80, 48, 903, 57682],
                                   [30, 2, 26, 442, 10, 18, 10]]

    try:
        m = m1 + m2
    except IndexError:
        pass

    print("Add test complete")


def test_sub():
    """
    Осуществляет проверку вычитания двух матриц (работы функции sub).
    :return: "Sub test complete".
    """
    assert (m1 - m3).to_list() == [[-3, -2, 0, 1, 0, 0, 0], [0, 0, 0, -62, 0, 0, 0], [0, 0, 0, -60, 0, 0, 0],
                                   [0, 0, -20, -420, 0, 0, 0]]
    assert (m1 - m4).to_list() == [[-3, -2, 0, 1, 0, 0, 0], [2, 1, 0, 4, 0, 0, 0], [-121, 0, 0, -60, -38, -891, -57670],
                                   [0, 0, -20, -420, 0, 0, 0]]

    try:
        m = m1 - m2
    except IndexError:
        pass

    print("Sub test complete")


def test_mul():
    """
    Осуществляет проверку умножения двух матриц или матрицы на число (работы функции mul).
    :return: "Multiply test complete".
    """
    assert (m1 * m1).to_list() == [[62, 8, 28, 78], [62, 14, 46, 126], [152, 14, 46, 144], [167, 30, 94, 215]]
    assert (m1 * m3).to_list() == [[62, 8, 108, 2000], [68, 18, 126, 2286], [152, 14, 246, 4586], [212, 60, 314, 5062]]

    try:
        m = m1 * m2
    except IndexError:
        pass

    print("Multiply test complete")


def test_slice():
    """
    Осуществляет проверку вывода строк и столбцов матрицы (работы функции getitem).
    :return: "Slice test complete".
    """
    assert m1[0:1:] == [[0, 1, 3, 4, 5, 6, 6]]
    assert m2[0:1:] == [[3, -5]]

    try:
        m = m1[0:1000:]
        m = m1[1, 43]
        m = m1['a']
        m = m1[100]
    except TypeError:
        pass

    print("Slice test complete")


def test_transposition():
    """
    Осуществляет проверку транспонирования матрицы (работы функции trans).
    :return: "Transposition test complete".
    """
    assert m1.trans().to_list() == [[0, 2, 0, 15], [1, 1, 1, 1], [3, 7, 3, 3], [4, 4, 10, 11], [5, 5, 5, 5],
                                    [6, 9, 6, 9], [6, 6, 6, 5]]
    assert m3.trans().to_list() == [[3, 2, 0, 15], [3, 1, 1, 1], [3, 7, 3, 23], [3, 66, 70, 431], [5, 5, 5, 5],
                                    [6, 9, 6, 9], [6, 6, 6, 5]]
    try:
        assert m1.trans().to_list() == [1, 2]
    except AssertionError:
        pass

    print("Transposition test complete")


def test_delete():
    """
    Осуществляет проверку удаления строки или столбца матрицы (работы функции delete).
    :return: "Delete test complete".
    """
    assert m1.delete("строка", 1).to_list() == [[2, 1, 7, 4, 5, 9, 6], [0, 1, 3, 10, 5, 6, 6], [15, 1, 3, 11, 5, 9, 5]]
    assert m1.delete("столбец", 1).to_list() == [[1, 3, 4, 5, 6, 6], [1, 7, 4, 5, 9, 6], [1, 3, 10, 5, 6, 6],
                                                 [1, 3, 11, 5, 9, 5]]

    try:
        m1.delete(10, 1)
    except IndexError:
        pass

    print("Delete test complete")


def test_determinant():
    """
    Осуществляет проверку нахождения детерминанта матрицы (работы функции invert).
    :return: "Determinant test complete".
    """
    assert ~m2 == -1

    try:
        assert ~m1
    except ValueError:
        pass

    print("Determinant test complete")


def test_size():
    """
    Осуществляет проверку нахождения размера матрицы (работы функции size).
    :return: "Size test complete".
    """
    assert m1.size() == f"{len(m1.to_list())} строк, {len(m1.to_list()[0])} столбцов"

    try:
        m1.size() == 12
    except AssertionError:
        pass

    print("Size test complete")


def test_permutation():
    """
    Осуществляет проверку перестановки строк или столбцов матрицы (работы функции permutation).
    :return: "Permutation test complete".
    """
    assert m1.permutation("строка", 1, 2).to_list() == [[2, 1, 7, 4, 5, 9, 6], [0, 1, 3, 4, 5, 6, 6],
                                                        [0, 1, 3, 10, 5, 6, 6], [15, 1, 3, 11, 5, 9, 5]]

    try:
        m = m1.permutation("строка", 1, 70)
    except IndexError:
        pass

    print("Permutation test complete")


def test_reverse():  # **(-1)
    """
    Осуществляет проверку нахождения обратной матрицы (работы функции pow).
    :return: "Reverse test complete".
    """
    assert (m2 ** -1).to_list() == [[2, -5], [1, -3]]

    try:
        m = m1 ** -1
    except numpy.linalg.LinAlgError:
        pass

    print("Reverse test complete")


def test_rang():
    """
    Осуществляет проверку нахождения ранга матрицы (работы функции rang).
    :return: "Rang test complete".
    """
    assert m1.rang() == 4
    assert m2.rang() == 2
    assert m3.rang() == 4
    assert m4.rang() == 4

    try:
        assert m1.rang() == 1
    except AssertionError:
        pass

    print("Rank test complete")


def test_to_list():
    """
    Осуществляет проверку вывода матрицы как массив (работы функции to_list).
    :return: "Matrix to array test complete".
    """
    assert m1.to_list() == array1
    assert m2.to_list() == array2
    assert m3.to_list() == array3
    assert m4.to_list() == array4

    try:
        assert m1.to_list() == [1, 2, 3]
    except AssertionError:
        pass

    print("Matrix to array test complete")


test_add()
test_sub()
test_mul()
test_slice()
test_transposition()
test_delete()
test_determinant()
test_size()
test_permutation()
test_rang()
test_to_list()