import analyzeTadin

subjectID = 'gbaby_combined'


inputtedContrasts = []
#inputtedContrasts = [2, 99]
inputtedTargetRadii = []
#inputtedTargetRadii = np.array([1.33, 2.33, 4, 7, 12])*0.5

comparison = 'targetXVelocities-mouseXVelocities'
load = False

peaks, contrasts, targetRadii = analyzeTadin.analyzeTadin(subjectID, inputtedContrasts, inputtedTargetRadii, comparison, load)