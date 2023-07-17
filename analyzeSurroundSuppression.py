import analyzeContinuous
import matplotlib.pyplot as plt

subjectID = 'harry_200ms'
experimentName = 'experiment_2_simplified'
contrasts = [2, 8, 16]
spatialFrequency = 1

peaks = []
for cc in contrasts:
    peak, lag, width_fwhm = analyzeContinuous.analyzeContinuous(subjectID, experimentName, cc, spatialFrequency)
    peaks.append(peak)
    
#contrast = 16
#analyzeContinuous.analyzeContinuous(subjectID, experimentName, contrast, spatialFrequency)

plt.plot(log(contrasts), peaks)