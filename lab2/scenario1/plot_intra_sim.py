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

fig, (p1,p2,p3) = plt.subplots(3,1,sharex=False, sharey=False)

df['mean_speed'].hist(ax=p1)
p1.set_title("Avg speed (m/s) - 20 runs of {} min".format(len(df) + 15))
p1.set_xlabel("Speed - m/s")
p1.set_ylabel("Frequency")

#df['cum_variance2'].plot(ax=p2, use_index=True)
#p2.set_xlabel("Minute")
#p2.set_ylabel("Variance - (m/s)^2")

# As we are running only 1 simulation, it does not make sense to divide it by R.
df['cum_variance'].plot(ax=p2, use_index=True)
p2.set_xlabel("Minute")
p2.set_ylabel("S. variance - (m/s)^2")

df['cum_departed'].plot(ax=p3, use_index=True)
p3.set_xlabel("Minute")
p3.set_ylabel("C. departed vehicles")
plt.show()
