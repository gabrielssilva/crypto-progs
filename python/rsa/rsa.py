

def gcd(a, b):
    while b:
        a, b = b, a%b
    return a


def phi(n):
    primes = 0
    for k in range(1, n+1):
        if gcd(k, n) == 1:
            primes += 1
    return primes


def extended_euclid(a, b):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        q = a // b
        x0, x1 = x1, x0 - (q * x1)
        y0, y1 = y1, y0 - (q * y1)
        a, b = b, a % b
    return  x0, y0


def cipher(block, e, n):
    return (block ** e) % n


def decipher(block, d, n):
    return (block ** d) % n


def run():
    print('Choose a value for p')
    p = int(input('>>> '))
    print('Choose a value for q')
    q = int(input('>>> '))

    n = p * q
    phi_n = phi(n)

    print('Choose a public key')
    e = int(input('>>> '))

    while(gcd(e, phi_n) != 1):
        print('The public key is invalid (gcd(%d, %d) != 1). Try again' %
              (e, phi_n))
        e = int(input('>>> '))

    d, _ = extended_euclid(e, phi_n)

    print('Which operation do yout want to perform?')
    print('[1] Cipher')
    print('[2] Decipher')
    while True:
        op = input('>>> ')
        if op is '1':
            operation = cipher
            key = e
            break
        if op is '2':
            operation = decipher
            key = d
            break
        else:
            print('Invalid operation. Try again')

    print('Enter the input file path')
    in_path = input('>>> ')
    print('Enter the output file path')
    out_path = input('>>> ')

    in_file = open(in_path, 'r')
    out_file = open(out_path, 'w')

    block = in_file.read(1)
    while block:
        out_block = operation(ord(block), key, n)
        out_file.write(chr(out_block))
        block = in_file.read(1)
    in_file.close()
    out_file.close()
