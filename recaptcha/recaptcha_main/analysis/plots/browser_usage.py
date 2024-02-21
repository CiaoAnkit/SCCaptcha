import matplotlib.pyplot as plt
import numpy as np
import textwrap
# Data
browsers = ['Chrome', 'Safari', 'Firefox', 'Edge', 'Opera', 'Samsung Internet', 'Brave']
world_stats = [64.38, 18.86, 3.3, 5.35, 2.56, 2.55, 1.00]  # as of Jan 2024
study_stats = [85.34, 3.4, 1.7, 0, 3.4, 6.03, 0] #for study 1
# study_stats = [59,2,3,1,1,0,7] #for study 2
# study_stats = [i/sum(study_stats)*100 for i in study_stats]
print(study_stats)
supported = ['\u2713', '\u2717', '\u2717', '\u2713', '\u2713', '\u2713', '\u2717']
# if yes calculate the percentage of users who support it
supported_people = [ study_stats[i]*107/100 if supported[i] == '\u2713' else 0 for i in range(len(supported))]
print(supported_people, sum(supported_people))
# X axis locations
x = np.arange(len(browsers))

# Width of the bars
width = 0.25
plt.rcParams.update({'font.size': 16})

# Plotting
plt.figure(figsize=(10, 6))

# plt.bar(x - width/2, world_stats, width, label='Market Share as of Jan, 2024')
# plt.bar(x + width/2, study_stats, width, label='as per user study among 116 users')
world_bars = plt.bar(x - width/2, world_stats, width,label='Market share as of Jan, 2024', hatch='//')
study_bars = plt.bar(x + width/2, study_stats, width,label='As per user study among 116 users', hatch='\\\\' )

# # Add line styles inside bars
# for i, bar in enumerate(world_bars):
#     plt.plot([bar.get_x() + bar.get_width()/2, bar.get_x() + bar.get_width()/2], [0, world_stats[i]], linestyle='--', color='black')

# for i, bar in enumerate(study_bars):
#     plt.plot([bar.get_x() + bar.get_width()/2, bar.get_x() + bar.get_width()/2], [0, study_stats[i]], linestyle=':', color='black')
# # Customizing the plot
plt.text(-0.5, -15, 'Support for \n our captcha:', fontsize=16, ha='right')

plt.xlabel('Browsers and their Support for our Captcha')
plt.ylabel('Percentage of users')
xvals = [browsers[i] + '             \n' + supported[i] for i in range(len(browsers))]
wrapped_labels = [textwrap.fill(label, width=10) for label in xvals]
plt.xticks(x, wrapped_labels, ha='center')
# plt.xtickslabels(supported, ha='center')
plt.yticks(np.arange(0, 101, 10))  # Set y-axis ticks from 0 to 100 with a step of 10

plt.legend()

plt.tight_layout()
plt.show()
