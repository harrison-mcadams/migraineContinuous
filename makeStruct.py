def makeStruct(listOfFields):

    nFields = len(listOfFields)

    if nFields == 1:
        fieldLevel0 = listOfFields[0]
        zeroCounter = 1
        for zero in fieldLevel0:
            if zeroCounter == 1:
                struct = {zero: []}
            else:
                struct.update({zero: []})
            zeroCounter = zeroCounter + 1



    if nFields == 2:

        fieldLevel0 = listOfFields[0]
        fieldLevel1 = listOfFields[1]

        zeroCounter = 1
        for zero in fieldLevel0:
            if zeroCounter == 1:
                struct = {zero: []}
            else:
                struct.update({zero: []})
            zeroCounter = zeroCounter + 1

            oneCounter = 1
            for one in fieldLevel1:
                if oneCounter == 1:
                    struct[zero] = {one: []}
                else:
                    struct[zero].update({one: []})
                oneCounter = oneCounter + 1

    if nFields == 3:

        fieldLevel0 = listOfFields[0]
        fieldLevel1 = listOfFields[1]
        fieldLevel2 = listOfFields[2]

        zeroCounter = 1
        for zero in fieldLevel0:
            if zeroCounter == 1:
                struct = {zero: []}
            else:
                struct.update({zero: []})
            zeroCounter = zeroCounter + 1

            oneCounter = 1
            for one in fieldLevel1:
                if oneCounter == 1:
                    struct[zero] = {one: []}
                else:
                    struct[zero].update({one: []})
                oneCounter = oneCounter + 1

                twoCounter = 1

                for two in fieldLevel2:
                    if twoCounter == 1:
                        struct[zero][one] = {two: []}
                    else:
                        struct[zero][one].update({two: []})
                    twoCounter = twoCounter + 1


    if nFields == 4:

        fieldLevel0 = listOfFields[0]
        fieldLevel1 = listOfFields[1]
        fieldLevel2 = listOfFields[2]
        fieldLevel3 = listOfFields[3]

        zeroCounter = 1
        for zero in fieldLevel0:
            if zeroCounter == 1:
                struct = {zero: []}
            else:
                struct.update({zero: []})
            zeroCounter = zeroCounter + 1

            oneCounter = 1
            for one in fieldLevel1:
                if oneCounter == 1:
                    struct[zero] = {one: []}
                else:
                    struct[zero].update({one: []})
                oneCounter = oneCounter + 1

                twoCounter = 1

                for two in fieldLevel2:
                    if twoCounter == 1:
                        struct[zero][one] = {two: []}
                    else:
                        struct[zero][one].update({two: []})
                    twoCounter = twoCounter + 1

                    threeCounter = 1
                    for three in fieldLevel3:
                        if threeCounter == 1:
                            struct[zero][one][two] = {three: []}
                        else:
                            struct[zero][one][two].update({three: []})

                        threeCounter = threeCounter + 1

    return struct