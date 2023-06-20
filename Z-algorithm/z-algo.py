def zalgo(patt):
    """
    This algorithm outputs the z-array for the input string.
    Computes in O(n) time to be used for linear-time pattern matching 
    """
    pattlength = len(patt)
    z_array = [None] * pattlength   # set array with None values
    z_array[0] = pattlength         # first item in the array is string length 
    i = 1                           # set pointer to be 1, skipping the string length value 
    r, l = 0 , 0                    # left right pointers

    while i < pattlength: 

        #variables
        remaining = r-i+1
        k = i-l
        
        if i> r:    #case 1 outside box have to do implicit searching 
            x = 0 
            pointer = i
            if patt[x] == patt[i]:
                while pointer < pattlength and patt[x] == patt[pointer]:
                    l = i 
                    x += 1
                    pointer += 1
                z_array[i] = x  

            elif patt[i] != patt[x]:
                z_array[i] = 0
                
        else:
            if z_array[k] < remaining:   #case 2a
                z_array[i] = z_array[k]

            elif z_array[k] > remaining: #case 2b
                z_array[i] = remaining

            elif z_array[k] == remaining: #case 2c (have to do more specific computations when it is k == r)
                x = remaining
                while pointer < pattlength and  patt[x] == patt[pointer]:
                    l = i 
                    x += 1
                    pointer += 1
                z_array[i] = x  

        i+=1

    return z_array

