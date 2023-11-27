getSessionInfo
- subjectID, screenDistance, demoLogic

getExperimentParams

getTrialList

## Run demo
trials: high contrast and big, high contrast and small, low contrast big, low contrast small
demoTrialList = getTrialList('demo')
for tt in demoTrialList:
    runTrial(tt)

while continueDemo:
    continueDemo = askSubjectWhetherToContinue
    demoTrialList = getTrialList('manual')
    runTrial(demoTrialList)

## Run trials
trialList = getTrialList('session')
for tt in trialList:
    runTrial(tt)


runTrials