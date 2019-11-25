import pandas as pd
import sys

import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

csv_file = sys.argv[1]
df = pd.read_csv(csv_file, index_col=0)

#Variance2 = Variance of the sample mean
df['cum_variance2'] = df['cum_variance']/df.index

print(df)

print("Mean speed: {} m/s".format(df['mean_speed'].mean()))
print("Mean accel: {} m/s^2".format(df['mean_accel'].mean()))
print("Mean departed: {}".format(df['departed'].mean()))
print("Sample mean accel variance: {}".format(df['mean_accel'].var()/20))

fig, (p1,p2) = plt.subplots(2,1,sharex=False, sharey=False)

df['mean_speed'].hist(ax=p1)
p1.set_title("Mean speed and accel. distributions - {} runs".format(len(df)))
p1.set_xlabel("Speed - m/s")
p1.set_ylabel("Frequency")

df['mean_accel'].hist(ax=p2)
p2.set_xlabel("Accel - m/s^2")
p2.set_ylabel("Frequency")
'''
df['cum_variance2'].plot(ax=p3, use_index=True)
p3.set_xlabel("Simulation")
p3.set_ylabel("Variance - (m/s)^2")

df['departed'].plot(ax=p4, use_index=True)
p4.set_xlabel("Simulation")
p4.set_ylabel("Departed vehicles")
'''
plt.show()
