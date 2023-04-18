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


def AdjustAmbient(DesiredColour:Colour):
    
    # get the sensor colour
    r, g, b = 225, 80, 72

    # average out the components of both colours
    sens = ConvertSensorRGB(r, g, b)
    newcol = Colour()

    for i in range(3):
        temp = DesiredColour[i]*2 - sens[i]
        if temp < 0:
            temp = 0
        elif temp > 255:
            temp = 255
        newcol[i] = temp

    print(newcol)

    
    
    """            Color c1 = label2.BackColor;
        Color c2 = label3.BackColor;

        int[] rgb = {(c1.R + c2.R)/2, (c1.G + c2.G) / 2 , (c1.B + c2.B) / 2 };

        // the Average value
        label5.BackColor = Color.FromArgb(rgb[0], rgb[1], rgb[2]);

        // the average value set to 100%
        while (rgb.Max() < 255)
        {
            for (int i = 0; i < rgb.Length; i++)
            {
                rgb[i]++;
            }
        }

        label4.BackColor = Color.FromArgb(rgb[0], rgb[1], rgb[2]);"""
    

AdjustAmbient(Colour(21, 45, 60))
        
# SaveSteps()
# ReadSteps()
        




