import numpy as np

# 4x5の乱数配列を作成
a = np.random.random((4, 5))
print(a)

# 整数による要素の選択
print('スライスによる要素の選択')
print('4x5行列aの真ん中の2x3=6個の値を取り出す。')
center = a[1:3, 1:4]
print(center)

print('真ん中の6個の値を0とする。')
a[1:3, 1:4] = 0
print(a)

# 整数配列による要素の選択
b = np.array(
  [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
  ]
)

print(np.array([b[0, 1], b[2, 1], b[1, 0]]))
print(b[[0, 2, 1], [1, 1, 0]])

# if np.array([b[0, 1], b[2, 1], b[1, 0]]) == b[[0, 2, 1], [1, 1, 0]]:
#   print('equal')

print('ndarray型のデータ')
# 整数（pythonのint型）の要素を持つリストを与えた場合
x = np.array([1, 2, 3])
print(x.dtype)

x = np.array([1., 2., 3.])
print(x.dtype)

x = np.array([1, 2, 3], dtype = 'float32')
print(x.dtype)

# 短く書くには
x = np.array([1, 2, 3], dtype = 'f')
print(x.dtype)

# TODO:明日確認
# データ型を変更するには
# x = np.astype(np.float64)
# print(x.dtype)
