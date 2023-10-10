import random
import math
import sys

def binaryConverter(num):
    """
    Convert a decimal number to binary, output is stored in a list, but results is in reverse
    """
    binary = []
    while num > 0:
        binary.append(num % 2)
        num = num // 2
    return binary

def ModExpo(decimal, exponential, modulo):
    """
    Modular exponentiation with repeated squaring 
    """
    current = 0
    counter = 0
    repeated_squaring = []
    
    #Get the binary bits of the exponential 
    exponential = binaryConverter(exponential)
    
    #Pre-compute all of the binary numbers in 'exponential'
    for i in range(0, len(exponential)):
        repeated_squaring.append(decimal ** (2**i) % modulo) 

    #After everything is computed, then use the expression 'x.y mod z' to obtain final answer
    for i in range(0, len(exponential)):
        if exponential[i] == 1 and counter == 0 :
            current= repeated_squaring[i]
            counter = 1
        elif exponential[i] == 1 and counter != 0:
            current = current * repeated_squaring[i] % modulo
            
    return current
 
def MillerRabinRandomizedPrimality(n,k):
    """
    Miller-Rabins Randomized Primality testing algorithm, taken from lectures 
    """
    #Since k is in decimal, need to convert it into non decimal
    k = math.floor(k)
    
    if n % 2 == 0 or (n % 3 == 0 and n != 3):
        return False

    if n == 2 or n == 3:
        return True
    
    s = 0
    t = n - 1
    while t % 2 == 0:
        s =+ 1
        t = t//2

    for i in range(k):
        
        a = random.randint(2, n-2)
        x = ModExpo(a, n-1, n)
        
        #Check x satisfies Fermat's little theorem
        if x != 1:
            return False

        #Recomputation using repeated squaring
        previous = ModExpo(a, (2**0)*t, n)

        #Sequence test 
        for j in range(1,s):
            current = (previous * previous) % n
            if current == 1 and (previous != 1 and previous != n-1):
                return False

            #If current value is 1, then the previous values will also equal to one 
            if current == 1:
                break
            previous = current

    return True

def GCD(x, y):
    """
    Basic Euclid algorithm
    """
    if x == 0:
        return y
 
    return GCD(y % x, x)

def generate_primes(x):
    """
    Function to generate prime numbers p and q using Miller Rabin 
    """
    p = None
    q = None
    while x <= 2000 and (p == None or q == None) :
        k = math.log(x) #Let k be dynamic
        if MillerRabinRandomizedPrimality((2**x)-1, k) == True: 
            if p == None and q == None:
                p = (2**x)-1
            elif p != None and q == None:
                q = (2**x)-1
        x += 1
    return p, q

def generate_exponent(p, q):
    """
    Function to generate the exponent 
    """
    lam = ((p-1) * (q-1)) // GCD(p-1,q-1)
    exponent = random.randint(3, lam) #Dont use lamda-1 and end range because randint(start, stop+1)
    
    #Exponent is chosen until GCD(e,lambda) == 1
    while GCD(exponent, lam) != 1:
        exponent = random.randint(3, lam)
    return exponent

def generate_key(d):
    """
    Function to generate everything before reading into file
    """
    p,q = generate_primes(d)
    e = generate_exponent(p, q)
    n = p * q
    return p,q,e,n 

def write_file(data):
    p,q,e,n = generate_key(data)
    output_PK = open("publickeyinfo.txt", "w")
    output_PK.write("# modulus (n) \n")
    output_PK.write(str(n) + "\n")
    output_PK.write("# exponent (e) \n")
    output_PK.write(str(e) + "\n")
    output_PK.close()

    output_SP = open("secretprimes.txt", "w")
    output_SP.write("# p \n")
    output_SP.write(str(p) + "\n")
    output_SP.write("# q \n")
    output_SP.write(str(q) + "\n")
    output_SP.close()

if __name__=="__main__":
    input_specs = sys.argv[1]
    write_file(int(input_specs))

