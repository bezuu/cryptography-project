import DES as d

def hex2bin(s):
    """
    Przekształcamy tekst z systemu szesnastkowego na binarny.
    :param s: Tekst w systemie szesnastkowym.
    :return: Tekst w systemie binarnym.
    """
    mp = {'0': "0000",
          '1': "0001",
          '2': "0010",
          '3': "0011",
          '4': "0100",
          '5': "0101",
          '6': "0110",
          '7': "0111",
          '8': "1000",
          '9': "1001",
          'A': "1010",
          'B': "1011",
          'C': "1100",
          'D': "1101",
          'E': "1110",
          'F': "1111"}
    text = ""
    for i in range(len(s)):
        text = text + mp[s[i]]
    return text

def permIP(block):
    """
    Permutacja 64-bitowego bloku za pomocą permutacji IP.
    :param block: Blok, który ma zostać spermutowany.
    :return: Spermutowany blok.
    """
    Block = ''
    for i in range(64):
        Block = Block + block[d.IP[i]-1]
    return Block

def permIPReverse(block):
    """
    Permutacja 64-bitowego bloku za pomocą permutacji IP.
    :param block: Blok, który ma zostać spermutowany.
    :return: Spermutowany blok.
    """
    Block = ''
    for i in range(64):
        Block = Block + block[d.IPReverse[i]-1]
    return Block

def functionE(block):
    """
    Działanie funkcji E na 32-bitowy blok.
    :param block: Blok, który ma zostać poddany działaniu funkcji E.
    :return: Wynik działania funkcji E na podany blok. Wynik ma 48-bitów.
    """
    Block = ''
    for i in range(48):
        Block = Block + block[d.TableE[i]-1]
    return Block

def permP(block):
    """
    Permutacja 32-bitowego bloku za pomocą permutacji IP.
    :param block: Blok, który ma zostać spermutowany.
    :return: Spermutowany blok.
    """
    Block = ''
    for i in range(32):
        Block = Block + block[d.P[i]-1]
    return Block

def PermutedChoice1(key):
    """
    Funkcja najpierw dzieli klucz na dwa 28-bitowe bloki,
    a następnie je permutuje.
    :param key: Klucz, na który chcemy zadziałać tą funkcją.
    :return: Zwracany jest wygenerowany klucz lewy i prawy, oba mają
    po 28-bitów.
    """
    KeyLeft = ''
    KeyRight = ''
    for i in range(28):
        KeyLeft = KeyLeft + key[d.PC1[i] - 1]
    for i in range(28,56):
        KeyRight = KeyRight + key[d.PC1[i] - 1]
    return (KeyLeft,KeyRight)



def LeftShift(key, number_iteration):
    """
    Przesuwamy 28 bitów klucza w lewo. Liczba przesunięć zależna jest
    od numeru iteracji.
    :param key: Klucz, który chcemy przesunąć.
    :param number_iteration: Numer rundy, w której jest generowany klucz.
    :return: Zwracany jest przesunięty klucz.
    """
    Shift = d.LeftShifts[number_iteration]
    Key = ''
    for i in range(Shift,28):
        Key = Key + key[i]
    for i in range(Shift):
        Key = Key + key[i]
    return Key

def PermutedChoice2(keyLeft,keyRight):
    """
    Funkcja wybiera 48 bitów z dwóch 28-bitowych kluczy.
    :param keyLeft: Klucz lewy.
    :param keyRight: Klucz prawy.
    :return: 48-bitowy klucz.
    """
    Key = ''
    key = keyLeft + keyRight
    for i in range(48):
        Key = Key + key[d.PC2[i] - 1]
    return Key

def SBox(block):
    """
    Funkcja działa na podany block 8 S-Boxami.
    :param block: 48-bitowy blok wejściowy.
    :return: 32-bitowy blok po wyniku działania 8 S-Boxów.
    """
    Output = ''
    k=0
    for i in range(0,48,6):
        Block = block[i:i+6]
        Raw = int(Block[0]+Block[5], 2)
        Column = int(Block[1:5],2)
        liczba = format(d.S[k][Raw][Column],'b')
        liczba = str(0)*(4 - len(liczba)) + liczba
        Output = Output + liczba
        k +=1
    return Output

def enrycpt(block,key):
    """
    Funkcja szyfruje podany blok, przy za pomocą podanego klucza.
    :param block: Blok tekstu, który chcemy zaszyfrować.
    :param key: Klucz, którym chcemy zaszyfrować tekst.
    :return: Zaszyfrowany tekst.
    """
    if len(block) != 64 or len(key) != 64:
        return ("Błędna długość bloku lub kodu")
    block = permIP(block)
    block_left = block[0:32]
    block_right = block[32:64]
    key_left, key_right = PermutedChoice1(key)
    for i in range(16):
        key_left = LeftShift(key_left,i)
        key_right = LeftShift(key_right,i)
        Key = PermutedChoice2(key_left,key_right)
        block_right1 = functionE(block_right)
        block_right1 = format(int(block_right1, 2) ^ int(Key,2),'b')
        block_right1 = str(0) * (48 - len(block_right1)) + block_right1
        block_right1 = permP(SBox(block_right1))
        block_right1 = format(int(block_right1, 2) ^ int(block_left,2),'b')
        block_right1 = str(0)*(32 - len(block_right1)) + block_right1
        block_left = block_right
        block_right = block_right1
        if i == 15:
            block_right = block_left
            block_left = block_right1
    block = block_left + block_right
    return permIPReverse(block)


plaintext ='123456ABCD132536'
key = 'AABB09182736CCDD'

def decrypt(block,key):
    """
    Funkcja odszyfrowuje podany blok tekstu, za pomocą klucza.
    :param block: Blok tekstu, który chcemy odszyfrować.
    :param key: Klucz, za pomocą którego, chcemy odszyfrować wiadomość.
    :return: Odszyfrowana wiadomość.
    """
    if len(block) != 64 or len(key) != 64:
        return ("Błędna długość bloku lub kodu")
    block = permIP(block)
    block_left = block[0:32]
    block_right = block[32:64]
    key_left, key_right = PermutedChoice1(key)
    keys = []
    for i in range(16):
        key_left = LeftShift(key_left, i)
        key_right = LeftShift(key_right, i)
        keys.append(PermutedChoice2(key_left, key_right))

    block_right1 = functionE(block_right)
    block_right1 = format(int(block_right1, 2) ^ int(keys[15], 2), 'b')
    block_right1 = str(0) * (48 - len(block_right1)) + block_right1
    block_right1 = permP(SBox(block_right1))
    block_right1 = format(int(block_right1, 2) ^ int(block_left, 2), 'b')
    block_right1 = str(0) * (32 - len(block_right1)) + block_right1
    block_left = block_right1
    block_right = block_right
    for i in range(15):
        Key = keys[14-i]
        block_right1 = functionE(block_left)
        block_right1 = format(int(block_right1, 2) ^ int(Key,2),'b')
        block_right1 = str(0) * (48 - len(block_right1)) + block_right1
        block_right1 = permP(SBox(block_right1))
        block_right1 = format(int(block_right1, 2) ^ int(block_right,2),'b')
        block_right1 = str(0)*(32 - len(block_right1)) + block_right1
        block_right = block_left
        block_left = block_right1
    block = block_left + block_right
    return permIPReverse(block)


def TripleDesEncrypt(block, key1, key2, key3):
    """
    Funkcja szyfruje 64-bitowy blok tekstu algorytmem 3DES za pomocą trzech kluczy.
    :param block: Blok tekstu, który chcemy zaszyfrować algorytmem 3DES.
    :param key1: Pierwszy klucz.
    :param key2: Drugi klucz.
    :param key3: Trzeci klucz.
    :return: Tekst zaszyfrowany algorytmem 3DES.
    """
    return enrycpt(decrypt(enrycpt(block,key1), key2),key3)

def TripleDesDecrypt(block, key1, key2, key3):
    """
    Funkcja odszyfrowuje 64-bitowy blok tekstu algorytmem 3DES za pomocą trzech kluczy.
    :param block: Blok tekstu, który chcemy odszyfrować.
    :param key1: Pierwszy klucz.
    :param key2: Drugi Klucz.
    :param key3: Trzeci Klucz.
    :return: Tekst odszyfrowany algorytmem 3DES.
    """
    return decrypt(enrycpt(decrypt(block,key3),key2),key1)
\