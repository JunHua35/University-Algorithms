import sys

def tableau_method(dv, constraints, objectives, LHS, RHS):
    """
    Linear Programming Tableau Method
    Returns a list of RHS values, maximised Z value, objectives and the coefficient array
    """
    #Initialize an array for the coefficient of each non_basic variable. Here all will be 0
    coefficients = []
    for i in range(0, constraints):
        coefficients.append(0)
        
    #Check to see if all values in the Cj-Zj array are positive integers, if not can exit loop
    terminate = True

    #Initialize the first Cj array 
    cj = objectives
    for i in range(0,constraints):
        cj.append(0)

    #Put in the number of 0's needed for the number of non-basic variables
    for i in range(0, constraints):
        LHS[i]+= [0 for m in range(constraints)]
        LHS[i][i + dv] = 1

    #Initialize the first Cj-Zj array 
    cz  = []
    for i in range(constraints+dv):
        cz.append(None)
    
    max_positive = None
    chosen_column = None
    z = 0
    #Compute the Cj-Zj array
    for i in range(0, (constraints+dv)):
        maximum = cj[i]
        for j in range(0, constraints):
            maximum -= LHS[j][i] * coefficients[j]
            if i == 0:
                z += RHS[j] * coefficients[j] 
        #The column with the largest positive integer of Cj-Zj will be used for the next iteration
        if maximum > 0:
            #If the integer exists, dont need to terminate earlier 
            if terminate:
                terminate = False

            #The largest value in Cj, with the index of the chosen column   
            chosen_column = i  
            max_positive = maximum

        cz[i] = maximum

    #Early termination condition 
    if terminate:
        return coefficients, RHS, objectives, z

    #Initialize a theta value
    theta = RHS[0] / LHS[0][chosen_column]
    
    #Calulate the remaining theta values for all of the RHS values
    row = 0
    for i in range(1, constraints):
        #Find the row of the non-basic variable that needs to be swapped with the chosen basic variable
        if LHS[i][chosen_column]!= 0 and RHS[i] / LHS[i][chosen_column] > 0 and RHS[i] / LHS[i][chosen_column] < theta:
            theta = RHS[i] / LHS[i][chosen_column] 
            row = i      

    #Update the coefficeint array since we have swapped rows 
    coefficients[row] = cj[chosen_column]

    #Continue to calculate the subqsequent iterations to obtain the optimal X and Y values 
    while not terminate:
        terminate = True
        cross_section = LHS[row][chosen_column] #The cross section value thats needed to find the next row swap
        z = 0 #reset the z value 
                
        #Initialize an array to store the old LHS values   
        old_LHS = []
        for i in range(0, (constraints)):
            old_LHS.append([None])
            for j in range(0, constraints+dv):
                old_LHS[i].append(None)
        #insert the values from LHS into it, so that we have a reference list   
        for i in range(0, len(LHS)):
            for j in range(0, len(LHS[0])):
                old_LHS[i][j] = LHS[i][j]
                LHS[i][j] = None #Change the inserted LHS values into None so the next iteration can store inside
        
        #Do the same for the RHS values 
        old_RHS = []
        for i in range(0, constraints):
            old_RHS.append(None)
        for i in range(0, len(RHS)):
            old_RHS[i] = RHS[i]
            RHS[i] = None
        
        #Put in the chosen row into the now empty LHS list 
        for i in range(0, (dv+constraints)):
            LHS[row][i] = old_LHS[row][i] / cross_section
        #Also do the same for RHS
        RHS[row] = old_RHS[row] / cross_section

        #Now fill in the other values of the matrix and RHS values by using the equation T = J - K      
        for i in range(0, constraints):
            if i != row:
                for j in range(0, (dv+constraints)):
                    LHS[i][j] = old_LHS[i][j] - (old_LHS[i][chosen_column] *LHS[row][j])
                RHS[i] = old_RHS[i] - (old_LHS[i][chosen_column] *RHS[row])

        #Compute the subsequent Cj-Zj array
        CjZj = []
        for i in range(0, constraints+dv):
            CjZj.append(None)
        
        #Reset these values to compute the Cj-Zj array
        chosen_column = None
        max_positive = None 

        #Compute the Cj-Zj array by inserting the dot product of the columns
        for i in range(0,constraints+dv):
            maximum = cj[i] 
            for j in range(0,constraints):
                maximum -= LHS[j][i] * coefficients[j]
                if i == 0:
                    z += RHS[j] * coefficients[j]
            if maximum > 0:
                if terminate:
                    terminate = False
                chosen_column = i
                max_positive = maximum
            CjZj[i] = maximum
        
        #If the maximum value is <= 0, then the current Z value is the maximised Z, break out of loop
        if terminate:
            break
        
        #If the maximum value > 0, then continue iterating 
        theta = RHS[0] / LHS[0][chosen_column]
        row = 0
        for i in range(1, constraints):
            if LHS[i][chosen_column]!= 0 and RHS[i] / LHS[i][chosen_column] > 0 and RHS[i] / LHS[i][chosen_column] < theta:
                theta = RHS[i] / LHS[i][chosen_column] 
                row = i 
        
        #Update coefficients of the swapped objective rows as we iterate thru 
        coefficients[row] = cj[chosen_column]

    return coefficients, RHS, objectives, z

def read_file(input):
    with open(input) as file:
        next(file)
        dv = int(file.readline().replace('\n',''))

        next(file)
        constraints = int(file.readline().replace('\n',''))

        next(file)
        objectives = file.readline().replace('\n','').split(', ')
        for i in range(len(objectives)):
            objectives[i] = eval(objectives[i])

        next(file)
        LHS = [] #Store LHS values into a nested list 
        for _ in range(constraints):
            LHS_section = file.readline().replace('\n','').split(", ")
            for i in range(len(LHS_section)):
                LHS_section[i] = eval(LHS_section[i])
            LHS.append(LHS_section)

        next(file)
        RHS = []
        for _ in range(constraints):
            RHS.append(eval(file.readline().replace('\n','')))

    return dv, constraints, objectives, LHS, RHS

def write_file(dv, constraints, objectives, LHS, RHS):
    
    coefficients, RHS, objectives, z = tableau_method(dv, constraints, objectives, LHS, RHS)

    with open("lpsolution.txt", "w") as file:
        file.write("# optimalDecisions\n")
        max_values = ""
        for i in range(len(objectives)):
            for j in range(len(coefficients)):
                if coefficients[j] > 0 and coefficients[j] == objectives[i]:
                    max_values += f"{int(RHS[j])}, "
        max_values = max_values[:len(max_values) - 2]
        file.write(f"{max_values}\n")
        file.write("# optimalObjective\n")
        file.write(f"{int(z)}\n")

if __name__ == "__main__":
    input = sys.argv[1]
    dv, constraints, objectives, LHS, RHS = read_file(input)
    write_file(dv, constraints, objectives, LHS, RHS)

