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

def patternMatching(text,pattern):
    """
    This function finds the occurrences of the pattern that appears in the text.
    First value of the output list is the total number of occurrences of the pattern in the text 
    Time complexity: O(N) 
    Space complexity: O(N) 
    """
    lst = [0] 
    #Add the pattern before the text with terminal symbol in between them, then perform Z-algo on the string
    prefix = pattern+'$'+text
    ZalgoPrefix = zalgo(prefix)

    #Add the pattern after the text to get the reverse z-algo of the combined string
    suffix = text+'$'+pattern
    suffix = suffix[::-1]
    ZalgoSuffix = zalgo(suffix)

    #check the Prefix and the Suffix Zbox starting from the pattern
    ZalgoPrefix = ZalgoPrefix[len(pattern)+1:len(prefix)-len(pattern)+1]
    ZalgoSuffix = ZalgoSuffix[len(pattern)+1:len(prefix)-len(pattern)+1]
    
    #Reverse the ZalgoSuffix array so comparism can be done with the ZalgoPrefix array to find the transposition error
    ZalgoSuffix = ZalgoSuffix[::-1]

    #Comparing the 2 Zbox array,if there is a matching value means there is an occurance of the pattern
    for i in range(len(ZalgoPrefix)):
        #Find position of the occurrance of pattern in the text 
        if ZalgoSuffix[i] + ZalgoPrefix[i] == 2*len(pattern):
            lst.append((i+1))

    lst[0] = len(lst)-1 #set the total number of occurrences to first index of the list 
    return lst
