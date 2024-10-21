from gtts import gTTS
import pygame

myText = 'Keep Still'
language = 'en'
myobj = gTTS(text=myText, lang=language, slow=False)
myobj.save("keepStill.mp3")
pygame.mixer.int()
pygame.mixer.music.load("keepStill")
pygame.mixer.music.play()
