== Dependências ==

Estes programas foram escritos em Python3. Para executá-los, é necessário
possuir a versão 3 do interpretador Python isntalado, bem como a biblioteca
matemática NumPy.

Confira a versão do Python e instale o NumPy, de preferência em um ambiente
virutal (vritualenv ou similar):

$ python --version
$ pip install numpy

== Instruções de Execução ==

a partir da página raiz do projeto (src), os módulos podem ser executados
diretamente com o python. Tanto o AES quando o modo CFB já possuem valores de
teste iniciados, e vão imprimir os resultados para os valores padrão que podem
ser encontrados no código. No entanto, os programas também podem ser executados
em modo interativo, possibilitando a execução de outros testes.

=== Executando o AES ===

Inicie o programa no modo interativo:

$ python -i -m aes.aes

Resultados preliminares serão impressos, mas o console estará disponível para
demais procedimentos. Algumas instâncias já estão disponíveis no console:

* key: uma chave no formato esperado (0f1571c947d9e8590cb7add6af7f6798)
* cipher: cifrador AES configurado com a chave acima
* decipher: decifrador AES configurado com a chave acima

Para criar uma nova chave, e novos cifradores e decifradores:

> key = block_from_hex("0f1571c947d9e8590cb7add6af7f6798")
> aes_key = AESKey(key)
> cipher = AESCipher(aes_key)
> decipher = AESDecipher(aes_key.inverse())

Para cifrar e decifrar textos:

> secret = cipher.compute_str("input plaintext")
> decipher.compute_str(secret)

=== Executando o CFB ===

Inicie o programa no modo interativo:

$ python -i -m block_operations.cfb

Assim como o programa do AES, alguns resultados serão impressos, mas é possível
realizar mais testes no console interativo. Neste caso, as instâncias já
disponíveis são:

* iv: um vetor de inicialização representado como um numero inteiro
  (0123456789abcdeffedcba9876543210 em hexadecimal)
* key: chave no formato esperado (0f1571c947d9e8590cb7add6af7f6798)
* cfb_cipher: cifrador em modo CFB configurado com key e iv
* cfb_decipher: decifrador em modo CFB configurado com key e iv

Para criar uma nova chave, iv, e novos cifradores e decifradores:

> iv = int("0123456789abcdeffedcba9876543210", 16)
> key = block_from_hex("0f1571c947d9e8590cb7add6af7f6798")
> aes_key = AESKey(key)
> cipher = AESCipher(aes_key)
> cfb_cipher = CFBCipher(cipher, iv)
> cfb_decipher = CFBDecipher(cipher, iv)

Para cifrar e decifrar textos:

> secret = cfb_cipher.compute_str("input plaintext")
> cfb_decipher.compute_str(secret)
