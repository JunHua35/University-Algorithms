# Public key generation 

Inspired by the [RSA public-key encryption system](https://en.wikipedia.org/wiki/RSA_(cryptosystem)); this algorithm two integers, modulus n and exponent e, as a public key. 

To generate the modulus and exponent, the algorithm has implented:
1. Modular exponentiation with repeated squaring method
2. Miller-Rabin randomized primality test with appropriate level of confidence that the test is probably correct
3. Euclid algorithm to compute the greatest common divisor of any two numbers

Arguments to your program: input integer d ≥ 1 \
Command line usage of your script: ` python mykeygen.py <d> ` 

There will be 2 output files:
1. publickeyinfo.txt giving information of the modulus n and exponent e.
2. secretprimes.txt giving the information of the two primes p and q
