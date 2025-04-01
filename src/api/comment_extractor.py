import os
import googleapiclient.discovery



def extract_comments(video_url, max_comments=50):

    comments = [
    "This video is amazing! Learned so much!",  
    "Great content as always. Keep it up!",  
    "Not sure I agree with this point, but interesting take.",  
    "Wow! This was super helpful. Thanks a lot!",  
    "I don’t get the hype around this topic.",  
    "Best tutorial I’ve seen on this subject!",  
    "I’m confused. Can you clarify at 3:25?",  
    "This changed my perspective completely!",  
    "Meh, nothing new here.",  
    "You explained it so well. Subscribed!",  
    "The editing is top-notch!",  
    "I wasted my time watching this.",  
    "Very insightful. Keep making more!",  
    "Haters gonna hate, but this was great!",  
    "I love the way you explain things!",  
    "Not sure if I understood everything, but trying my best.",  
    "Can you make a video on a related topic?",  
    "This deserves more views!",  
    "Terrible explanation. Thumbs down.",  
    "I found this really helpful, thanks!",  
    "Amazing work! Keep going!",  
    "This is exactly what I was looking for.",  
    "Disappointed. Expected better.",  
    "Funny and informative at the same time!",  
    "Why does this not have more likes?",  
    "Your videos always make my day better!",  
    "I have a question, can you help?",  
    "This video helped me pass my exam!",  
    "Not bad, but could be improved.",  
    "Super entertaining and educational!",  
    "I never miss a video from you!",  
    "Annoying background music.",  
    "Perfect explanation. Thank you!",  
    "Too fast, can you slow down next time?",  
    "This is a masterpiece!",  
    "I don’t understand, but I’ll try again.",  
    "Clear and concise, love it!",  
    "Why is this video not viral yet?",  
    "One of the best videos I’ve watched!",  
    "I disagree with some points, but well done.",  
    "Total waste of time.",  
    "This should be in the recommended section!",  
    "You just earned a new subscriber!",  
    "Amazing visuals and content!",  
    "I wish I found this video earlier!",  
    "Such a great breakdown of the topic!",  
    "I laughed so hard at 2:34!",  
    "You made this topic so easy to understand!",  
    "Not really my cup of tea.",  
    "This deserves an award!",  
    "This video has a lot of potential!"  
    ]

    return comments