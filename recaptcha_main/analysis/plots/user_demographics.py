import matplotlib.pyplot as plt
# Define the data
labels = ['18-24', '25-30', '>30']
sizes = [80/107, 25/107, 2/107]
# labels = ['Male', 'Female']
# sizes = [87/107,20/107]
# colors = ['lightblue', 'lightgreen', 'lightcoral']
# explode = (0.1, 0, 0)  # explode the first slice (18-24)
# linestyles = ['-', '--', ':']  # Different line styles for each age group

# Plot
plt.rc('font', size=24)

plt.figure(figsize=(6, 8))
patches, texts, attexts = plt.pie(sizes, autopct='%1.1f%%')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
patches[0].set_hatch('/')
patches[1].set_hatch('\\')
# patches[2].set_hatch('|')
for text in attexts:
    text.set_color('white')
# Create a legend with color-coded labels
plt.legend( labels, loc="upper left")
# plt.pie(sizes, labels=labels, autopct='%1.1f%%')
# plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()
plt.savefig('age.png')




