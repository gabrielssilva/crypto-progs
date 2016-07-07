

def extended_euclid(a, b):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        q = a // b
        x0, x1 = x1, x0 - (q * x1)
        y0, y1 = y1, y0 - (q * y1)
        a, b = b, a % b
    return  x0, y0


def find_points(E):
    points = []
    for x in range(0, E['p']):
        for y in range(0, E['p']):
            left_expr = (y**2) % E['p']
            right_expr = (x**3 + E['a']*x + E['b']) % E['p']
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
        x = (e_lambda**2 - q[0] - r[0]) % E['p']
        y = (e_lambda * (q[0] - x) - q[1]) % E['p']
        return (x, y)


def find_point_order(q, E):
    result = sum_points(q, q, E)
    order = 2
    while result != (0, 0):
        result = sum_points(result, q, E)
        order += 1
    return order


def run():
    print("Choose a value for a")
    a = int(input(">>> "))

    print("Choose a value for b")
    b = int(input(">>> "))

    print("Choose a value for p")
    p = int(input(">>> "))

    E = { 'a': a, 'b': b, 'p': p }
    points = find_points(E)
    points = [{ 'point': q, 'order': find_point_order(q, E) } for q in points]

    max_order = max(points, key=lambda q: q['order'])['order']
    max_order_points = [q['point'] for q in points if q['order'] == max_order]

    print(points)
    print('There are %d points in this curve' % len(points))
    print('The greatest order is %d' % max_order)
    print('The following points have order %d:' % max_order)
    print(max_order_points)


if __name__ == '__main__':
    run()
