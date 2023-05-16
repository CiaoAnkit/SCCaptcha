# ReCap

### Captcha Design

![image-20230516001323369](/home/cyk/.config/Typora/typora-user-images/image-20230516001323369.png)

User moves the ball from the centre towards the upright image going around the obstacles. User can guide the ball by tilting their mobile device appropriately. On hovering over the right image, the captcha is passed, otherwise if hovered over other image, the captcha fails prompting the user to try again. If the user fails to solve the captcha in 10 seconds, the captcha resets itself to a new one. 



#### Prevention from attackers

This captcha is designed keeping in mind various automated bots. The difficulty lies recognizing the upright image and finding a path to it avoiding the obstacles. The captcha image is randomly picked from a large collection, rotated at some random multiple of rightangle, and is sent to the frontend which places 4 rotated images in the captcha marked by unique ids. Both the captcha box id on which the ball hovers and the path taken by the ball tracked at a particular frequency is sent to the backend server. The path taken by the ball is verified in the backend server, making sure that distance two adjacent track points are less than a given threshold (set as max velocity of ball/ frequency of tracking). Then the end point the track is verified whether it lies in the correct upright image.





```python
def verify_path(path,user_id):
    obs = user_data[user_id]['obs']
    captcha_box = user_data[user_id]['captcha_box'][user_data[user_id]['ans']]
    pathlen = len(path)
    if pathlen <= 2:
        return False
    prevpoint = path[0]
    for i in range(1,pathlen):
        for corner in obs:
            if inbox(path[i],corner):
                return False
        dist_trav = dist(prevpoint,path[i])
        if dist_trav > THRESHOLD:
            return False
        prevpoint = path[i]
    if not inbox(path[-1],captcha_box):
        return False
    return True
```

​      