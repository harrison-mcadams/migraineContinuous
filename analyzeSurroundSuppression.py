import analyzeContinuous

subjectID = '500ms'
experimentName = 'experiment_2_simplified'
contrast = 16
spatialFrequency = 1

analyzeContinuous.analyzeContinuous(subjectID, experimentName, contrast, spatialFrequency)

contrast = 2
analyzeContinuous.analyzeContinuous(subjectID, experimentName, contrast, spatialFrequency)
