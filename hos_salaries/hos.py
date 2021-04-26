import xlrd
import numpy as np
import matplotlib.pyplot as plt

# Import seaborn
import seaborn as sns

# Set dark grid
sns.set()

book = xlrd.open_workbook("hos_salaries\\data.xls")
sheet = book.sheet_by_name("All")
N = sheet.nrows

states = [sheet.cell_value(r, 0) for r in range(1, N)]
hos_salaries = [sheet.cell_value(r, 1) for r in range(1, N)]
hog_salaries = [sheet.cell_value(r, 2) for r in range(1, N)]

final_hos_salaries = [hos_salaries[s] for s,d in enumerate(hog_salaries) if isinstance(d,float)]
for s in range(len(final_hos_salaries)):
    if final_hos_salaries[s] == '':
        final_hos_salaries[s] = 0

final_hog_salaries = [int(s) for s in hog_salaries if isinstance(s,float)]
final_states = [states[s] for s,d in enumerate(hog_salaries) if isinstance(d,float)]

final_hog_salaries, final_states = zip(*sorted(zip(final_hog_salaries, final_states)))

final_hog_salaries = final_hog_salaries[-10:]
final_states = final_states[-10:]
print(final_states)
# print(final_hog_salaries, final_states)

n_groups = len(final_hog_salaries)

# create plot
fig, ax = plt.subplots()
bar_width = 0.5
opacity = 0.8

y_pos = np.arange(len(final_hog_salaries))
hog = plt.barh(y_pos+bar_width, final_hog_salaries, alpha=opacity, label='Head of Government')
plt.tight_layout()
plt.yticks(y_pos+bar_width, final_states, fontsize=12)
plt.xticks(ticks=range(0,2000000,250000))
plt.xlabel('Head of Government Salary (USD)')
plt.ticklabel_format(style='plain', axis='x')
plt.title('Salaries of European Heads of Government (USD)')

for i, v in enumerate(final_hog_salaries):
    plt.text(v + 10000, i + 0.4, '$' + str(v), color='black')

# for rect, label in zip(hog, final_hog_salaries):
#     w = rect.get_width()
#     plt.text(rect.get_y() + rect.get_height()/2.0, w + 5, label, ha='left', va='center')

plt.show()



