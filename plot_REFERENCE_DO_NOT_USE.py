import sys
import pandas as pd
import random as rand
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

# Error for inputs
if len(sys.argv) != 7:
    print("ERROR: ONLY SEVEN ARGUMENTS ALLOWED")
    sys.exit()

# Read in inputs
filename = sys.argv[1]
rows = int(sys.argv[2])
cols = int(sys.argv[3])
middle = int(sys.argv[4]) - 1
headerRows = int(sys.argv[5])
headerCols = int(sys.argv[6])

# Constant for hard-coded y-margin
# This has to be done so the separation line can be drawn neatly
# This is never used in the margin method - it is used to compute the max sizes on the upper line graph
ymargin = 0.1

# Constant for x-margin
# This is used within the margin method
xmargin = 0.0

# Generate the header/column lists for reading the .txt file as .csv
headerRowList = []
for i in range(headerRows):
    headerRowList.append(i)
headerColList = []
for i in range(headerCols):
    headerColList.append(i)

# Read in the text file as .csv, as well as making a .csv file
df1 = pd.read_csv(filename, sep='\s+', header=headerRowList, index_col=headerColList)
df1.to_csv(filename[0:len(filename) - 4] + ".csv")

for name in list(df1.columns.values):
    print(name)

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(rows, cols))

fake_feature_data = []
for i in range(0, 195):
    fake_feature_data.append(i * rand.random())
testdf = pd.DataFrame(fake_feature_data)
testdf = testdf.transpose()
print(testdf)

# NOTE - NOW YOU WOULD HAVE TO MATCH THE FEATURE DATA INDIVIDUAL TO THE OTHER INDIVIDUALS



# Creating different color map objects
colors = ["blue", "White", "red"]
#colors = ["#E66100", "#5D3A9B"]
#colors = ["#FEFE62", "#D35FB7"]
#colors = ["#FEFE62", "#FFFFFF", "#D35FB7"]
#colors = ["#1AFF1A", "#4B0092"]
#colors = ["#1AFF1A", "#FFFFFF", "#4B0092"]
#colors = ["#E1BE6A", "#FFFFFF", "#40B0A6"]
cmap1 = LinearSegmentedColormap.from_list("mycmap", colors)
cmap1.set_over("#8b0000")

maximum_value = df1.values.max()
minimum_value = df1.values.min()

im = ax2.imshow(df1, aspect = 'auto', cmap = cmap1, vmax = maximum_value * 0.85)
ax2.margins(x = 0.0, y = 0.0)
#ax2.plot([middle + 0.5, middle + 0.5], [-0.5, rows - 0.5], color = 'black')
ax2.set_yticks([])
ax2.set_xticks([])
fig.colorbar(im, ax=ax2, orientation='horizontal', cmap = cmap1)

im2 = ax3.imshow(testdf, aspect = 'auto')

# Used this as a resource for normalization
# https://stackoverflow.com/questions/26414913/normalize-columns-of-a-dataframe
normalized_df1 = (df1-df1.min())/(df1.max()-df1.min())

# Used this as a resource for mean centering
# https://www.appsloveworld.com/pandas/100/439/how-to-do-mean-centering-on-a-dataframe-in-pandas
mean_centered_df1 = normalized_df1 - normalized_df1.mean()

# Get the medians for the data frame
# https://erikrood.com/Python_References/pandas_column_average_median_final.html
pd_medians = mean_centered_df1.median()

mean_centered_df1.T.plot(ax=ax1, alpha = 0.4, color = "red")

medians = []

for i in pd_medians:
    print("Median value", i)
    medians.append(i)

# Plot median values
ax1.plot(medians, color = 'black', linestyle = "dashed")

ax1.margins(x = xmargin, y = 0.0)
ax1.legend().remove()
min = min(mean_centered_df1.min())
max = max(mean_centered_df1.max())
ax1.set_ylim(min - ymargin, max + ymargin)

#ax1.plot([middle + 1.0, middle + 1.0], [min, max], color = 'black')
ax1.plot([0, cols], [0, 0], color='black', alpha=0.2)
ax1.set_facecolor((1, 1, 0.9))
ax1.set_xticks([])

# Used this
# https://www.tutorialspoint.com/drawing-lines-between-two-plots-in-matplotlib
middleLine = ConnectionPatch((middle + 1.0, max + ymargin), (middle + 0.5, rows - 0.5), coordsA = "data", coordsB = "data", axesA = ax1, axesB = ax2)

ax2.add_artist(middleLine)

plt.subplots_adjust(hspace=0.0)

plt.show()