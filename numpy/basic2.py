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
