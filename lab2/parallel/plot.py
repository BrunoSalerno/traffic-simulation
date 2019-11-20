import pandas as pd
import numpy as np
import sys

import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

csv_file = sys.argv[1]
df = pd.read_csv(csv_file)
df['sim'] = df.index + 1
df.set_index('sim')

#Variance2 = Variance of the sample mean
variances = []
for i in range(1, len(df.index) + 1):
    sample = df['mean_speed'].iloc[:i]
    variances.append(np.var(sample)/(i))

df['cum_variance2'] = variances

print(df)

print("Mean speed: {} m/s".format(df['mean_speed'].mean()))

fig, (p1,p2,p3) = plt.subplots(3,1,sharex=False, sharey=False)

df['mean_speed'].hist(ax=p1)
p1.set_title("Avg speed (m/s) - {} runs".format(len(df)))
p1.set_xlabel("Speed - m/s")
p1.set_ylabel("Frequency")

df['cum_variance2'].plot(ax=p2, use_index=True)
p2.set_xlabel("Simulation")
p2.set_ylabel("Variance - (m/s)^2")

df['departed'].plot(ax=p3, use_index=True)
p3.set_xlabel("Simulation")
p3.set_ylabel("Departed vehicles")
plt.show()
