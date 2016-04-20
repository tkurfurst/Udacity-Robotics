def test(N):
	t = 0.
	for i in range(N):
		t += float(i)
		"""
		if i == 1000:
			return ValueError, "hit 1000"
		"""
	return t
N = 10**6
print N, test(N)