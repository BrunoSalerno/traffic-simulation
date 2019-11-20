from scipy import stats
import sys
import pandas as pd

def t_test():
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    col = sys.argv[3]

    df1 = pd.read_csv(filename1, index_col=0)
    df2 = pd.read_csv(filename2, index_col=0)

    t,p = stats.ttest_ind(df1[col], df2[col])
    print("T-statistic: {}".format(round(t,2)))
    print("P-value: {}".format(round(p,6)))

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: mean_equality.py dataset1.csv dataset2.csv column_name")
        sys.exit(-1)

    t_test()
