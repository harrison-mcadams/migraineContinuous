def getSubjectInfo():

    subjectID = input('Enter SubjectID: ')
    viewingDistanceFlag = True
    while viewingDistanceFlag:

        viewingDistance_cm = input('Enter viewing distance (cm): ')

        try:
            if int(viewingDistance_cm) < 20 or int(viewingDistance_cm) > 100:
                print('Please enter a valid viewing distance in centimeters (cm)')
            else:
                viewingDistance_cm = int(viewingDistance_cm)
                viewingDistanceFlag = False

        except:
            print('Please enter a valid viewing distance in centimeters (cm)')

    return subjectID, viewingDistance_cm