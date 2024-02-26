import matplotlib.pyplot as plt
import numpy as np
import textwrap
# Data
browsers = ['Chrome', 'Safari', 'Firefox', 'Edge', 'Opera', 'Samsung Internet', 'Brave']
world_stats = [64.38, 18.86, 3.3, 5.35, 2.56, 2.55, 1.00]  # as of Jan 2024
study_stats = [85.34, 3.4, 1.7, 0, 3.4, 6.03, 0] #for study 1
study_stats2 = [59,2,3,1,1,0,7] #for study 2
study_stats2 = [i/sum(study_stats)*100 for i in study_stats2]
print(study_stats)
supported = ['\u2713', '\u2717', '\u2717', '\u2713', '\u2713', '\u2713', '\u2717']
# if yes calculate the percentage of users who support it
supported_people = [ study_stats[i]*107/100 if supported[i] == '\u2713' else 0 for i in range(len(supported))]
print(supported_people, sum(supported_people))
# X axis locations
x = np.arange(len(browsers))
auto_bars = int(input('Do you want to add labels on the bars? (1/0)'))

# Width of the bars
width = 0.25
plt.rcParams.update({'font.size': 18})

# Plotting
plt.figure(figsize=(10, 6))

#plot 3 bars and labels on each bar
world_bars = plt.bar(x - width, world_stats, width, label='Market share as of Jan, 2024', hatch='//')
study_bars = plt.bar(x, study_stats, width, label='As per user study among 116 users', hatch='\\\\' )
study_bars2 = plt.bar(x + width, study_stats2, width, label='As per user study among 107 users', hatch='--' )

# # Add line styles inside bars
# for i, bar in enumerate(world_bars):
#     plt.plot([bar.get_x() + bar.get_width()/2, bar.get_x() + bar.get_width()/2], [0, world_stats[i]], linestyle='--', color='black')

# for i, bar in enumerate(study_bars):
#     plt.plot([bar.get_x() + bar.get_width()/2, bar.get_x() + bar.get_width()/2], [0, study_stats[i]], linestyle=':', color='black')
# # Customizing the plot
if auto_bars == True:
    def autolabel(bars):
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2., height, '%d' % int(height),
                    ha='center', va='bottom')

    autolabel(world_bars)
    autolabel(study_bars)
    autolabel(study_bars2)
plt.text(-0.5, -18, 'Support for \n SCCaptcha:', fontsize=18, ha='right')

plt.xlabel('Browsers and their Support for SCCaptcha')
plt.ylabel('Percentage of users')
xvals = [browsers[i] + '                      \n\n' + supported[i] for i in range(len(browsers))]
wrapped_labels = [textwrap.fill(label, width=10) for label in xvals]
plt.xticks(x, wrapped_labels, ha='center')
# plt.xtickslabels(supported, ha='center')
plt.yticks(np.arange(0, 101, 10))  # Set y-axis ticks from 0 to 100 with a step of 10

plt.legend()

plt.tight_layout()
plt.show()
