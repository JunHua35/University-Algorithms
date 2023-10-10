# Public key generation 

Inspired by the [RSA public-key encryption system](https://en.wikipedia.org/wiki/RSA_(cryptosystem)), this algorithm two integers, modulus n and exponent e, as a public key.\ 
The steps you need to follow to generate n and e are described in the corresponding sections below

Arguments to your program: input integer d ≥ 1 \
Command line usage of your script: ` python mykeygen.py <d> ` 

There will be 2 output files:
1. publickeyinfo.txt giving information of the modulus n and exponent e.
2. secretprimes.txt giving the information of the two primes p and q
