import matplotlib.pyplot as plt
import textwrap
import numpy as np
import pandas as pd
# Data
ratings = [1, 2, 3, 4, 5]

text_captcha  = [9,6,15,19,27]
touch_captcha = [7,2,7,24,36]
rotate_captcha = [6,4,8,12,9]
#convert into percentages
text_captcha = [i/sum(text_captcha)*100 for i in text_captcha]
touch_captcha = [i/sum(touch_captcha)*100 for i in touch_captcha]
rotate_captcha = [i/sum(rotate_captcha)*100 for i in rotate_captcha]
# df = pd.DataFrame({'Text Captcha': text_captcha, 'Touch Captcha': touch_captcha, 'Rotate Captcha': rotate_captcha}, index=ratings)

ind = ['Text Captcha', 'Touch Captcha', 'Rotate Captcha']
rating1 = [text_captcha[0], touch_captcha[0], rotate_captcha[0]]
rating2 = [text_captcha[1], touch_captcha[1], rotate_captcha[1]]
rating3 = [text_captcha[2], touch_captcha[2], rotate_captcha[2]]
rating4 = [text_captcha[3], touch_captcha[3], rotate_captcha[3]]
rating5 = [text_captcha[4], touch_captcha[4], rotate_captcha[4] ]
df = pd.DataFrame({'Highly prefer the given': rating1, 'Would rather prefer the given': rating2, 'Equal preference for both': rating3, 'Would rather prefer SCCaptcha': rating4, 'Highly prefer  SCCaptcha': rating5}, index=ind)
plt.rcParams.update({'font.size': 18})
#write values inside 

ax = df.plot.barh(stacked=True)
ax.figure.set_size_inches(10, 5)
ax.set_ylabel('Given Captcha Type')
ax.set_xlabel('Percentage of Users')
plt.xlim(0, 100)

for idx, bar in enumerate(ax.patches):
    width = bar.get_width()
    height = bar.get_height()
    x, y = bar.get_xy()
    ax.annotate(f'{width:.1f}%', (x + width / 2, y + height / 2), ha='center', va='center', color='white', rotation = 45)

legend = plt.legend(loc='lower center', bbox_to_anchor=(0.5, 1.05), fancybox=True, ncol=5, markerscale=3)
for text in legend.get_texts():
    text.set_text(textwrap.fill(text.get_text(), width=18))
plt.show()
