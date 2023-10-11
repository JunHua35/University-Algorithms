"""
Boyer-Moore string-searching algorithm
"""
import sys

def zalgo(patt):
    """
    Z-algorithm 
    """
    pattlength = len(patt)
    z_array = [None] * pattlength   
    z_array[0] = pattlength        
    i = 1                           
    r, l = 0 , 0                    
    while i < pattlength: 
        remaining = r-i+1
        k = i-l
        
        if i> r:    
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
            if z_array[k] < remaining:
                z_array[i] = z_array[k]

            elif z_array[k] > remaining: 
                z_array[i] = remaining

            elif z_array[k] == remaining: 
                x = remaining
                while pointer < pattlength and  patt[x] == patt[pointer]:
                    l = i 
                    x += 1
                    pointer += 1
                z_array[i] = x  

        i+=1

    return z_array

def ExtendedBadCharacter(pattern):
    """
    Function for finding bad character in O(1) time 
    O(KM) time where K is the number of unique characters
    O(KM) space 
    """
    #Initialize the Matrix for all the alphabets
    EBC_matrix = [None] * 26
    
    #Create the matrix for unique characters only, and fill up matrix with 0's
    for i in range(len(pattern)):
        #ord(char) - 97 to put in the characters lexicographically
        if pattern[i] != ".":
            EBC_matrix[ord(pattern[i]) - 97] = [0] * len(pattern)
    
    return EBC_matrix



def GoodSuffix(pattern):
    #get the reverse zbox for the pattern
    pattRev = pattern[::-1]
    Zalgo = zalgo(pattRev)
    reversed_zarray = Zalgo[::-1] 

    temp_array = []
    GS_array = [0] * (len(pattern)+1)
    
    #setting up the GS array
    for i in range(len(reversed_zarray)-1):
        temp_array.append(len(pattern) - reversed_zarray[i]+1)
    for i in range(len(temp_array)):
        GS_array[temp_array[i]-1] = i+1

    # If a suffix is found in this index, append the suffix index where the suffix ends in the pattern
    suffix_array = []
    for i in range(1,len(pattern)):
        if reversed_zarray[i-1] !=0:
            if len(suffix_array) == 0:
                suffix_array.append(reversed_zarray[i-1])
            suffix_index2 = i - reversed_zarray[i-1]
            suffix_array.append(suffix_index2)

        suffix_index = len(pattern) - reversed_zarray[i-1]
        GS_array[suffix_index] = i
        if GS_array[i] != 0:
            suffix_array.append(i)

    #keep tracks of the suffix index that can occur in the pattern, store it in the first index since its not used
    GS_array[0] = suffix_array
    return GS_array

def MatchedPrefix(pattern):
    """
    Borrowed this from my previous assignment in 2022 Sem 1
    Coded this function referring to Ian's tutorials 
    """
    MP_array = zalgo(pattern)
    counter = 0
    #Find the index of the pattern where there are matching characters
    for i in range(len(MP_array) - 1, -1, -1):
        if MP_array[i] > counter and MP_array[i] + 1 == len(pattern) :
                counter = MP_array[i]
        MP_array[i] = counter

    return MP_array

def Boyer_Moore(text,pattern):
    """
    Average should be O(n/m), worse case O(n+m)
    """
    occurances = []  #Number of occurances of pattern in the text will be documented in here
    i = 0            #Index to shift left to right 
    shift = 1        #Distance where the pattern needs to shift (minimum 1) 

    #pointers to check for the start and end points of the matched pattern so we dont compare them again (for galil's optimization)
    galil_end = -1
    galil_start = -1
    
    #Preprocessing of the pattern for bad character, good suffix and matched prefix 
    EBC_matrix = ExtendedBadCharacter(pattern)
    GS_array = GoodSuffix(pattern)
    MP_array = MatchedPrefix(pattern)

    if len(pattern) == 0 or len(text) == 0 or len(pattern) > len(text):
        return occurances

    #Shifts pattern until it exceeds the text length 
    while i + len(pattern) <= len(text):
        k = len(pattern) - 1
        #Iterates thru the pattern backwards and compare the pattern char with the text char
        while k >= 0 and pattern[k] == text[k+i] :
            #Galil's optimization, when comparing pattern after the it has shifted, we skip this iteration because it has already been compared
            if k + i == galil_end:
                k = galil_start -i
            else:
                k -= 1

        #When k == -1 means there's a match, do matched prefix to see how far we need to jump   
        if k == -1:
            #Since we have found a match, append to the list
            occurances.append(k+i+2) 
            if len(pattern)> 1:
                jump = len(pattern) - MP_array[1] - 1
            else:
                jump = 1
            i += max(1,jump)
        
        #If k != -1, then there's a mismatch, here need to decide whether to do BC or GS
        else:
            #Get the index of the bad character in BC matrix
            BC_array = EBC_matrix[ord(text[k+i])-97]
             
            #Check if there are any mismatch char to the left of the pattern so we can skip those
            if BC_array is None:
                shift = len(pattern) - MP_array[k]
            else:
                #Keep track of the index of the right most BC 
                BC_index = BC_array[k]

                #Update the shift using the matched prefix if there are no index to shift
                if  MP_array[k] != 0 and BC_index == 0: 
                    shift = len(pattern) - MP_array[k]
                
                #Get the possible suffixes that can exist in the pattern, this will be used for comparing with BC later
                suffix_indexes = GS_array[0]
                #If suffixes dont exist and not BC index found, shift the whole pattern
                if  BC_index < 0 and len(suffix_indexes) == 0 :
                    shift = len(pattern) - 1   
                
                #If cannot find GS nad BC index, then shift by 1 index 
                elif   BC_index == 0 and MP_array[k] == 0: 
                    shift = 1

                #If both BC and GS exists, then choose the one which is larger skips
                else:
                    pointer = BC_index
                    #finds match in the possible suffix array
                    for j in range(len(suffix_indexes)-1,0,-1):
                        suffix = suffix_indexes[j]
                        #If the BC index comes before the GS index, then we sfhit to that index and set the galil optimization range
                        if suffix == BC_array[suffix]:
                            shift = (k + j) - suffix + 1
                            galil_end = suffix + shift + suffix_indexes[0] - 1
                            galil_start = suffix + shift -2

                        else: #check again on the BC index 
                            pointer = BC_array[pointer-1]
        
            i += shift   #the pattern will shift by whatever this value is 

    return occurances          

#Read the input file name 
def read_file(input_file):
    file = open(input_file, "r")
    read = file.read()
    file.close()
    return read

def write_file(BMW_file):
    output = open("output.txt", "w")
    for i in BMW_file:
        output.write(str(i) + "\n")
    output.close()
    with open("output.txt", "r") as file:
        data = file.read()
    print(data)

if __name__ == "__main__":
    arg1 = sys.argv[1]    
    arg2 = sys.argv[2]   
    output = Boyer_Moore(read_file(arg1), read_file(arg2))
    write_file(output)


