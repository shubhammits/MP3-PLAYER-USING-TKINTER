import os
from tkinter import *
import tkinter.messagebox
import time
import threading
from pygame import mixer
from tkinter import filedialog
from mutagen.mp3 import MP3
from tkinter import ttk
from ttkthemes import themed_tk as tk


root=tk.ThemedTk()
root.get_themes()
root.set_theme("radiance")   # plastik , clearlooks, radiance, scidmint, scidpink, scidgreen, black

#-------> Status Bar (Bottom)
statusbar1 = Label(root,text="Developed by @Shubham Nagariya", relief = SUNKEN,bg='#156451',fg='white',font='Times 15 bold')
statusbar1.pack(side = BOTTOM, fill = X)

statusbar = Label(root,text="Welcome to My MP3 Player", relief = SUNKEN, anchor = W)
statusbar.pack(side = BOTTOM, fill = X)

# Create Menu Bar
menubar = Menu(root)
root.config(menu=menubar)

# Create Sub-menu
subMenu = Menu(menubar,tearoff = 0)

playlist = []

# playlist - contains the full path + file name
# playlistbox - contains just the file name
# Full path + file name is required to play the music inside play_music load function

def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)

def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index,filename_path)
    index += 1

menubar.add_cascade(label="File",menu=subMenu)
subMenu.add_command(label="Open",command = browse_file)
subMenu.add_command(label="Exit",command=root.destroy)

def about_us():
    tkinter.messagebox.showinfo('About MP3 Player','This is a MP3 Player build using Python Tkinter by SHUBHAM !')

subMenu = Menu(menubar,tearoff = 0)
menubar.add_cascade(label="Help",menu=subMenu)
subMenu.add_command(label="About Us", command = about_us)


mixer.init()   # initializing The mixer
#root.geometry('400x300')
root.title("MP3 Player")
root.iconbitmap(r'images/favicon.ico')

# Root Window - Status bar, Left Frame, Rigth Frame
# Right Window - The list box (Play List)
# Left Window - Top Frame, Middle Frame, Bottom Frame

leftframe = Frame(root)
leftframe.pack(side=LEFT,padx=30)

playlistbox = Listbox(leftframe)
playlistbox.pack()

addbtn = ttk.Button(leftframe,text="Add",command=browse_file)
addbtn.pack(side=LEFT,padx=10)

def del_song():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)


delbtn = ttk.Button(leftframe,text="Remove",command=del_song)
delbtn.pack()

rightframe = Frame(root)
rightframe.pack()

topframe = Frame(rightframe)
topframe.pack()
#filelabel = Label(root,text='Lets make a noice..!')
#filelabel.pack(pady=10)

lengthlabel = Label(topframe,text='Total Length  : --:--',fg='#156451',font='Arial 10 bold')
lengthlabel.pack(pady=5)

currenttimelabel = Label(topframe,text='Current Time : --:--',relief = GROOVE,fg='#156451',font='Arial 10 bold')
currenttimelabel.pack()




def show_details(play_song):
    #filelabel['text'] = "Playing - " + '' + os.path.basename(filename)

    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()
    mins,secs = divmod(total_length,60)  #div - total_length/60, mod - total_length%60
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins,secs)
    lengthlabel['text'] = "Total Length : " + ' - ' + timeformat

    t1 = threading.Thread(target=start_count,args=(total_length,))
    t1.start()

    #start_count(total_length)

def start_count(t):
    global paused
    #------> mixer.music.get_busy() - Returns FALSE when we press the stop button (Music stop Playing)
    current_time=0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = "Current Time : " + ' - ' + timeformat
            time.sleep(1)
            current_time += 1


def play_music():
    global paused

    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing Music : " + '' + os.path.basename(play_it)
            show_details(play_it)
        except:
            #pass
            tkinter.messagebox.showerror('File not found','MP3 Player could not find the file, Please Try Again !')


def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music Stopped !"

paused = FALSE


def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music Paused !"


def rewind_music():
    play_music()
    statusbar['text'] = "Music Rewinded !"


def set_vol(val):
    volume = float(val)/100
    mixer.music.set_volume(volume)
    # set_volume of mixer takes value only from 0 to 1.

muted = FALSE
def mute_music():
    global muted
    if muted:   # UnMute the music
        mixer.music.set_volume(0.5)
        volumeBtn.configure(image=volumePhoto)
        volume.set(50)
        muted = FALSE
    else:       # Mute the music
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        volume.set(0)
        muted = TRUE


middleframe = Frame(rightframe)
middleframe.pack(pady=30,padx=30)

playPhoto = PhotoImage(file='images/play.png')
playBtn = ttk.Button(middleframe, image = playPhoto ,command = play_music)
playBtn.grid(row=0,column=0,padx=10)

stopPhoto = PhotoImage(file='images/stop.png')
stopBtn = ttk.Button(middleframe, image = stopPhoto ,command = stop_music)
stopBtn.grid(row=0,column=1,padx=10)

pausePhoto = PhotoImage(file='images/pause.png')
pauseBtn = ttk.Button(middleframe, image = pausePhoto ,command = pause_music)
pauseBtn.grid(row=0,column=2,padx=10)

#----> Bottom frame for volume, rewind, mutem etc

bottomframe = Frame(root)
bottomframe.pack()

rewindPhoto = PhotoImage(file='images/rewind.png')
rewindBtn = ttk.Button(bottomframe, image = rewindPhoto ,command = rewind_music)
rewindBtn.grid(row=0,column=0)

#----> Two images are put Here Mute & volume.
mutePhoto = PhotoImage(file='images/mute.png')
volumePhoto = PhotoImage(file='images/volume.png')
volumeBtn = ttk.Button(bottomframe, image = volumePhoto ,command = mute_music)
volumeBtn.grid(row=0,column=3)

volume = ttk.Scale(bottomframe,from_ = 0,to = 100,orient=HORIZONTAL,command = set_vol)
volume.set(50)
mixer.music.set_volume(0.5)
volume.grid(row=0,column=2,pady=15,padx=20)


def on_closing():
    #tkinter.messagebox.showinfo('Nice to enjoy with you',"Thank You !")
    stop_music()
    root.destroy()
root.protocol("WM_DELETE_WINDOW",on_closing)
root.mainloop()
