import pytest
from matrix import Matrix

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

m1 = Matrix(array1)
m2 = Matrix(array2)
m3 = Matrix(array3)
m4 = Matrix(array4)


def test_add():
    assert (m1 + m3).to_array() == [[3, 4, 6, 7, 10, 12, 12], [4, 2, 14, 70, 10, 18, 12], [0, 2, 6, 80, 10, 12, 12], [30, 2, 26, 442, 10, 18, 10]]
    assert (m1 + m4).to_array() == [[3, 4, 6, 7, 10, 12, 12], [2, 1, 14, 4, 10, 18, 12], [121, 2, 6, 80, 48, 903, 57682], [30, 2, 26, 442, 10, 18, 10]]

    with pytest.raises(IndexError):
        assert m1 + m2

    print("Add test complete")


def test_sub():
    assert (m1 - m3).to_array() == [[-3, -2, 0, 1, 0, 0, 0], [0, 0, 0, -62, 0, 0, 0], [0, 0, 0, -60, 0, 0, 0], [0, 0, -20, -420, 0, 0, 0]]
    assert (m1 - m4).to_array() == [[-3, -2, 0, 1, 0, 0, 0], [2, 1, 0, 4, 0, 0, 0], [-121, 0, 0, -60, -38, -891, -57670], [0, 0, -20, -420, 0, 0, 0]]
    with pytest.raises(IndexError):
        assert m1 - m2

    print("Sub test complete")


def test_mul():
    assert (m1 * m1).to_array() == [[62, 8, 28, 78], [62, 14, 46, 126], [152, 14, 46, 144], [167, 30, 94, 215]]
    assert (m1 * m3).to_array() == [[62, 8, 108, 2000], [68, 18, 126, 2286], [152, 14, 246, 4586], [212, 60, 314, 5062]]
    with pytest.raises(IndexError):
        assert m1 * m2

    print("Multiply test complete")


def test_slice():
    assert m1[0:1:] == [[0, 1, 3, 4, 5, 6, 6]]
    assert m2[0:1:] == [[3, -5]]
    with pytest.raises(TypeError):
        assert m1[1.2]
    with pytest.raises(TypeError):
        assert m1['a']
    with pytest.raises(TypeError):
        assert m1[6]

    print("Slice test complete")


def test_transposition():
    assert m1.trans().to_array() == [[0, 2, 0, 15], [1, 1, 1, 1], [3, 7, 3, 3], [4, 4, 10, 11], [5, 5, 5, 5], [6, 9, 6, 9], [6, 6, 6, 5]]
    assert m3.trans().to_array() == [[3, 2, 0, 15], [3, 1, 1, 1], [3, 7, 3, 23], [3, 66, 70, 431], [5, 5, 5, 5], [6, 9, 6, 9], [6, 6, 6, 5]]

    print("Transposition test complete")

def test_delete():
    assert m1.delete(1, 2).to_array() == [[2, 7, 4, 5, 9, 6], [0, 3, 10, 5, 6, 6], [15, 3, 11, 5, 9, 5]]
    assert m3.delete(1, 3).to_array() == [[2, 1, 66, 5, 9, 6], [0, 1, 70, 5, 6, 6], [15, 1, 431, 5, 9, 5]]
    with pytest.raises(IndexError):
        assert m1.delete(1, 9)
    with pytest.raises(IndexError):
        assert m3.delete(7, 1)

    print("Delete test complete")


def test_determinant():
    assert m2.__invert__() == -1

    print("Determinant test complete")


def test_size():
    assert m1.size() == f"{len(m1.to_array())} строк, {len(m1.to_array()[0])} столбцов"

    print("Size test complete")


def test_permutation():
    assert m1.permutation("строка", 1, 2).to_array() == [[2, 1, 7, 4, 5, 9, 6], [0, 1, 3, 4, 5, 6, 6], [0, 1, 3, 10, 5, 6, 6], [15, 1, 3, 11, 5, 9, 5]]
    with pytest.raises(IndexError):
        assert m1.permutation("Строка", 1, 65)
    with pytest.raises(IndexError):
        assert m3.permutation("Строка", 4, 17)

    print("Permutation test complete")


def test_reverse():  # **(-1)
    assert (m2 ** (-1)).to_array() == [[ 2 -5][ 1 -3]]
    with pytest.raises(ZeroDivisionError):
        assert m1 ** (-1)

    print("Reverse test complete")


def test_rang():
    assert m1.rang() == 4
    assert m2.rang() == 2
    assert m3.rang() == 4
    assert m4.rang() == 4

    print("Rank test complete")


def test_to_array():
    assert m1.to_array() == array1
    assert m2.to_array() == array2
    assert m3.to_array() == array3
    assert m4.to_array() == array4

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
test_to_array()