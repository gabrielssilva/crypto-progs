

def extended_euclid(a, b):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        q = a // b
        x0, x1 = x1, x0 - (q * x1)
        y0, y1 = y1, y0 - (q * y1)
        a, b = b, a % b
    return  x0, y0


def find_points(a, b, p):
    points = []
    for x in range(0, p):
        for y in range(0, p):
            left_expr = (y**2) % p
            right_expr = (x**3 + a*x + b) % p
            if left_expr == right_expr:
                points.append((x, y))
    return points


def find_lambda(q, r, E):
    if q == r:
        d, _ = extended_euclid((2 * q[1]), E['p'])
        return ((3 * q[0]**2 + E['a']) * d) % E['p']
    else:
        d, _ = extended_euclid((r[0] - q[0]), E['p'])
        return ((r[1] - q[1]) * d) % E['p']

def sum_points(q, r, E):
    if q[0] == r[0] and (q[1] % E['p']) == (-r[1] % E['p']):
        return (0, 0)
    else:
        e_lambda = find_lambda(q, r, E)
        print(e_lambda)
        x = (e_lambda**2 - q[0] - r[0]) % E['p']
        y = (e_lambda * (q[0] - x) - q[1]) % E['p']
        return (x, y)


def run():
    print("Choose a value for a")
    a = int(input(">>> "))

    print("Choose a value for b")
    b = int(input(">>> "))

    print("Choose a value for p")
    p = int(input(">>> "))

    points = find_points(a, b, p)
    print(points)

E = { 'a': 1, 'b': 1, 'p': 23 }
