# import matplotlib.pyplot as plt
# import textwrap
# import numpy as np
# # Data
# ratings = [1, 2, 3, 4, 5]
# values1 = [0, 1.7, 3.8, 56.4, 37.9]
# values = [0,5,16,42,13] #stdy2
# values = [i/sum(values)*100 for i in values]
# text = [ 'Very Difficult', 'Difficult', 'Moderate', 'Easy', 'Very Easy']

# plt.rcParams.update({'font.size': 18})
# width = 0.25

# # Plotting
# plt.figure(figsize=(10, 6))
# #plot bars beside each other for same x value
# x = np.arange(len(text))

# plt.bar(x-2*width, values1, label = 'Study1', width = width, hatch='//')
# plt.bar(x-width, values, label = 'Study2', width = width, hatch='\\\\')

# # plt.bar(ratings, values, label = 'Study2', hatch='//', width = width)
# # plt.bar(ratings, values1, label = 'Study1', hatch='\\\\', width = width)
# plt.xlabel('Easeness to understand and solve our captcha')
# plt.ylabel('Percentage of users')
# xtext = [ text[i]  for i in range(len(ratings))]
# wrapped_labels = [textwrap.fill(label, width=10) for label in xtext]

# print(xtext)
# plt.xticks(ratings, wrapped_labels, ha='center')
# plt.yticks(range(0, 70, 10))
# plt.legend()
# plt.show()
import matplotlib.pyplot as plt
import numpy as np

textratings = [1, 2, 3, 4, 5]
values1 = [0, 1.7, 3.8, 56.4, 37.9]
# values2 = [0, 5, 16, 42, 13]  # study2
values2 = [3,3,20,25,25]
values2_percentage = [i / sum(values2) * 100 for i in values2]  # Normalize values2 to percentages
text = ['Very Difficult', 'Difficult', 'Moderate', 'Easy', 'Very Easy']

# Set the width of the barsbar_
bar_width = 0.30
plt.rcParams.update({'font.size': 18})

# Set the x locations for the groups
index = np.arange(len(textratings))

# Plotting
plt.figure(figsize=(10, 6))

plt.bar(index - bar_width/2, values1, bar_width, label='Study 1', hatch='//')
plt.bar(index + bar_width/2, values2_percentage, bar_width, label='Study 2', hatch='\\\\')

plt.xlabel('Perceived Difficulty')
plt.ylabel('Percentage')
plt.xticks(index, text)  # Set text as x labels
plt.legend()
plt.tight_layout()
plt.show()
