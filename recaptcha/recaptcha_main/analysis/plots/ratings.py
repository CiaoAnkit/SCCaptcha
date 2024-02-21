import matplotlib.pyplot as plt
import textwrap
# Data
ratings = [1, 2, 3, 4, 5]
# values = [0, 1.7, 3.8, 56.4, 37.9]
values = [0,5,16,42,13] #stdy2
values = [i/sum(values)*100 for i in values]
text = [ 'Very Difficult', 'Difficult', 'Moderate', 'Easy', 'Very Easy']

plt.rcParams.update({'font.size': 16})
width = 0.25

# Plotting
plt.figure(figsize=(10, 6))
#plot bar graph
plt.bar(ratings, values, label = 'Usability of our captcha', hatch='//', width = width)
plt.xlabel('Easeness to understand and solve our captcha')
plt.ylabel('Percentage of users')
xtext = [ text[i]  for i in range(len(ratings))]
wrapped_labels = [textwrap.fill(label, width=10) for label in xtext]

print(xtext)
plt.xticks(ratings, wrapped_labels, ha='center')
plt.yticks(range(0, 70, 10))
plt.legend()
plt.show()
