from LEDStrip import Colour, ConvertSensorRGB

def SaveSteps():
    Steps = 112397
    MaxSteps = 112397
    try:
        with open("Steps.txt", 'w', encoding='utf-8-sig') as file:
            file.write(f'{Steps}\n')
            file.write(f'{MaxSteps}')

    except Exception as ex:
        print(f'The given filename "TEST_JSON_Steps.txt" yielded an exception of type {type(ex)}')
        print(f'Exception was {ex}')
        print('Fhe Candidates and their weighted odds were not loaded')
        
        
def ReadSteps():
    Steps = 99
    MaxSteps = 999
    try:
        with open("Steps.txt", 'r', encoding='utf-8-sig') as file:
            try:
                Steps = int(file.readline())
                MaxSteps = int(file.readline())
            except:
                print('Parsing the file did not work. WHOOPSIES!')

    except Exception as ex:
        print(f'The given filename "TEST_JSON_Steps.txt" yielded an exception of type {type(ex)}')
        print(f'Exception was {ex}')
        print('Fhe Candidates and their weighted odds were not loaded')
    
    print(f'Steps = {Steps}, MaxSteps = {MaxSteps}')


def AdjustAmbient(DesiredColour:Colour, r, g, b):
    
    # get the sensor colour
    # r, g, b = 255, 128, 64

    # average out the components of both colours
    # sens = ConvertSensorRGB(r, g, b)
    sens = Colour(r, g, b).NormalizeColour()

    DesiredColour.NormalizeColour()

    print(f'desired: {DesiredColour},\t sensor: {sens}')

    # newcol = Colour()

    # temps = []
    temps = Colour()
    

    for i in range(3):
        temps[i] = DesiredColour[i]*2 - sens[i]
        # temps.append(DesiredColour[i]*2 - sens[i])

    # print(temps)
    
    # newcol = ConvertSensorRGB(temps[0], temps[1], temps[2])
    newcol = temps.NormalizeColour()

    print (newcol)


    
def ColTest2():
    col = Colour(255, 210, 74)
    
    # for c in col:
    #     print(c)

    AdjustAmbient(col, 255, 128, 64)



def convertHexToCol(col) -> Colour:
    start = 1
    convCol = Colour()

    for i in range(3):
        print('0x' + col[start : start + 2])
        convCol[i] = int('0x' + col[start : start + 2], 16)
        start += 2

    return convCol


# ColTest2()

print(convertHexToCol('#554d80'))
        
# SaveSteps()
# ReadSteps()
        




