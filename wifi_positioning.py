from sympy import symbols, Eq, solve
import math

# Initialize x and y coordinates of our sensors.
xA = 0
yA = 0

xB = 6
yB = 8

xC = 5
yC = -12

# Read and transfer output.txt files into lists.
# Type where the output file's directory is located.
AP1 = open("/home/oem/Desktop/AP1_clear_value.txt", "r")
AP2 = open("/home/oem/Desktop/AP2_clear_value.txt", "r")
AP3 = open("/home/oem/Desktop/AP3_clear_value.txt", "r")

linesAP1 = AP1.readlines()
linesAP2 = AP2.readlines()
linesAP3 = AP3.readlines()

def findPosition(xA, yA, DistA, xB, yB, DistB, xC, yC, DistC, MAC):

    # Equation for getting x and y coordinates.
    x,y = symbols('x y')

    eq1 = Eq((xA-x)**2 + (yA-y)**2, DistA**2)
    eq2 = Eq((xB-x)**2 + (yB-y)**2, DistB**2)

    result = solve([eq1, eq2], [x, y])
    
    # Check is there any common roots between Eq. A and Eq. B, if no, looking up for root between Eq. A and Eq. C
    if result is not float:
        eq1 = Eq((xA-x)**2 + (yA-y)**2, DistA**2)
        eq2 = Eq((xC-x)**2 + (yC-y)**2, DistC**2)

        result = solve([eq1, eq2], [x, y])
        print(result)

        root1 = DistB**2 - ((xB-result[0][0])**2 + (yB-result[0][1])**2)
        root2 = DistB**2 - ((xB-result[1][0])**2 + (yB-result[1][1])**2)

        if abs(root1) < abs(root2):
            print(MAC, ":", result[0])
        else:
            print(MAC, ":", result[1])

    else:
        print(result)

        root1 = DistC**2 - ((xC-result[0][0])**2 + (yC-result[0][1])**2)
        root2 = DistC**2 - ((xC-result[1][0])**2 + (yC-result[1][1])**2)

        if abs(root1) < abs(root2):
            print(MAC, ":", result[0])
        else:
            print(MAC, ":", result[1])

# Compare output lists and concatenate common WiFi devices and their distance informations into new list.
concatenate_arr = []
for k in range(len(linesAP1)-1): 
    for l in range(len(linesAP2)-1):
        for m in range(len(linesAP3)-1):

            AP1_division = linesAP1[k].split("-")
            AP2_division = linesAP2[l].split("-")
            AP3_division = linesAP3[m].split("-")
            
            if AP1_division[0] == AP2_division[0] == AP3_division[0]:
                concatenate_arr.append(AP1_division[0] + "\n" + AP1_division[1] + AP2_division[1] + AP3_division[1])

# Send WiFi devices's BSSID and distance information to the positioning function.
for o in range(len(concatenate_arr)):
    
    concatenate_arr1 = concatenate_arr[o].split("\n")
    print(concatenate_arr[o])
    findPosition(xA, yA, float(concatenate_arr1[1]), xB, yB, float(concatenate_arr1[2]), xC, yC, float(concatenate_arr1[3]), str(concatenate_arr1[0]))

