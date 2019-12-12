p = [
  [17, -7, -11],
  [1, 4, -1],
  [6, -2, -6],
  [19, 11, 9],
]

v = [
  [0, 0, 0],
  [0, 0, 0],
  [0, 0, 0],
  [0, 0, 0],
]

for i in range(1000):
  # gravity

  for ai, a in enumerate(p):
    for bi, b in enumerate(p):
      if ai == bi:
        continue
      for d in [0, 1, 2]:
        apos = a[d]
        bpos = b[d]
        if apos < bpos:
          v[ai][d] += 1
          v[bi][d] -= 1
        elif bpos > apos:
          v[ai][d] -= 1
          v[bi][d] += 1
        else:
          pass
  # momentum
  for ai, a in enumerate(p):
    for d in [0, 1, 2]:
      p[ai][d] += v[ai][d]

  # print(p)

print(p)
s = 0

for ai, a in enumerate(p):
  vel = v[ai]
  pos = a

  s += sum([abs(_pos) for _pos in pos]) * sum([abs(_v) for _v in vel])
print(s)

# 40
# 11423
