import numpy as np

a = np.array([1, 2, 3])

print(a)
print('shapeとは、ndarrayのオブジェクトで多次元配列の形を保持している。')
print('ndimとは、ndarrayのオブジェクトで次元数を返す。')
print(a.shape)
print(a.ndim)

b = np.array(
  [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
  ]
)

print(b)
print('Shape:', b.shape)
print('Rank:', b.ndim)
print('sizeは、要素数を返す。')
print('size:', b.size)

# その他の配列作成方法
print('形を指定して、要素がすべて0で埋められたndarrayをつくる。')
c = np.zeros((3, 3))
print(c)

print('形を指定して、要素がすべて1で埋められたndarray')
d = np.ones((2, 3))
print(d)

print('形と値を指定して、要素が指定した値で埋められたndarray')
e = np.full((3, 2), 9)
print(e)

print('指定された大きさの単位行列をさらわすndarrayを作る。')
f = np.eye(5)
print(f)

print('形を指定して、0～1の間の乱数で要素を埋めたndarrayを作る。')
g = np.random.random((4, 5))
print(g)

print('3から始まり10になるまで1ずつ増加する数列を作る（10は含まない！）')
h = np.arange(3, 10, 1)
print(h)
