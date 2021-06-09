from tkinter import *
from tkinter import filedialog
import pygame
import time
from mutagen.mp3 import MP3

root = Tk()
root.title("MP3 Player")
root.geometry("500x400")
 
# ----------------------------------------------------PYGAME------------------------------------------------------------------
pygame.mixer.init()

# -----------------------------------------------------FONCTIONS-------------------------------------------------------

# FONCTIONS QUI GERE LE TEMPS
def play_time():
    current_time = pygame.mixer.music.get_pos()/1000
    # on va convertir current_time en une variable de temps en important time voir en haut
    converted_current_time = time.strftime('%H:%M:%S', time.gmtime(current_time))

    # TROUVER LA LONGUEUR DU MORCEAU
    # on récupère le nom du morceau
    song = playlist_box.get(ACTIVE)
    # On rajoute le texte pour avoir le lien complet
    song = f'c:/Users/eriol/Desktop/mplay/audio/{song}.mp3'
    # on crée une variable
    song_mut = MP3(song)
    global song_length
    song_length = song_mut.info.length # ça retourne un float de secondes qu'on va devoir convertir
    converted_song_length = time.strftime('%H:%M:%S', time.gmtime(song_length))

    # On grée un condition pour que le stop affiche bien le bon temps
    if current_time >= 1:
        # on intègre converted_current_timeà la status_bar
        status_bar.config(text=f"Temps: {converted_current_time} / {converted_song_length  }")
    # on appelle la fonction toutes les 1000ms
    status_bar.after(1000, play_time)





def add_song():
    song = filedialog.askopenfilename(initialdir="C:/Users/eriol/Desktop/mplay/audio",title="Choisir un morceau", filetypes= (("mp3 Files","*.mp3"),))
    # Décomposer le nom du morceau
    song = song.split("/")[-1].rsplit(".",1)[0]    
    playlist_box.insert(END, song)

def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir="C:/Users/eriol/Desktop/mplay/audio",title="Choisir un morceau", filetypes= (("mp3 Files","*.mp3"),))
    for song in songs:    
        # Décomposer le nom du morceau
        song = song.split("/")[-1].rsplit(".",1)[0]    
        playlist_box.insert(END, song)
       

def delete_song():
    playlist_box.delete(ANCHOR)

def delete_all_songs():
    playlist_box.delete(0, END)

def play():
    song = playlist_box.get(ACTIVE)
    song = f'c:/Users/eriol/Desktop/mplay/audio/{song}.mp3'
    
    # charger le morceau
    pygame.mixer.music.load(song)
    # jouer le morceau
    pygame.mixer.music.play(loops=0)
    play_time()


def stop():
    pygame.mixer.music.stop()
    # nettoyer la playlist
    playlist_box.selection_clear(ACTIVE)
    status_bar.config(text=f"Temps: 00:00:00 / 00:00:00  ")


# LA FONCTION PAUSE
# on crée une variable paused
global paused
paused = False

def pause(is_paused):
    global paused
    paused = is_paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True

def next_song():
    # on trouve le numero selectionné 
    next_one = playlist_box.curselection()
    # le suivant est le numero selectionné(indice 0 de la liste) + 1
    next_one = next_one[0] + 1
    # on récupère le nom du morceau
    song = playlist_box.get(next_one)
    # On rajoute le texte pour avoir le lien complet
    song = f'c:/Users/eriol/Desktop/mplay/audio/{song}.mp3'
    # on joue le suivant
    # charger le morceau
    pygame.mixer.music.load(song)
    # jouer le morceau
    pygame.mixer.music.play(loops=0)
    # on nettoie la playlist
    playlist_box.selection_clear(0,END)
    # on met a jour la selection de la playlist
    playlist_box.activate(next_one)
    playlist_box.selection_set(next_one, last=None)


def previous_song():
    # on trouve le numero selectionné 
    next_one = playlist_box.curselection()
    # le suivant est le numero selectionné(indice 0 de la liste) + 1
    next_one = next_one[0] - 1
    # on récupère le nom du morceau
    song = playlist_box.get(next_one)
    # On rajoute le texte pour avoir le lien complet
    song = f'c:/Users/eriol/Desktop/mplay/audio/{song}.mp3'
    # on joue le suivant
    # charger le morceau
    pygame.mixer.music.load(song)
    # jouer le morceau
    pygame.mixer.music.play(loops=0)
    # on nettoie la playlist
    playlist_box.selection_clear(0,END)
    # on met a jour la selection de la playlist
    playlist_box.activate(next_one)
    playlist_box.selection_set(next_one, last=None)









# Liste des morceaux
playlist_box = Listbox(root,bg="Black", fg="green", width=60, selectbackground="green",selectforeground="black",font=("Arial", 14))
playlist_box.pack(pady=10)

# --------------------------------------------les boutons de contrôles-------------------------------------------------------
# 3 on definit les images qu'on va assigner aux boutons
prev_btn_img = PhotoImage(file= "c:/Users/eriol/Desktop/mplay/images/prev.png")
next_btn_img = PhotoImage(file= "C:/Users/eriol/Desktop/mplay/images/next.png")
play_btn_img = PhotoImage(file= "C:/Users/eriol/Desktop/mplay/images/play.png")
pause_btn_img = PhotoImage(file= "C:/Users/eriol/Desktop/mplay/images/pause.png")
stop_btn_img = PhotoImage(file= "C:/Users/eriol/Desktop/mplay/images/stop.png")

# 1 on crée une frame 
control_frame = Frame(root)
control_frame.pack(pady=10)

# 2 les boutons 
prev_button = Button(control_frame, image=prev_btn_img, borderwidth=0, command= previous_song)
next_button = Button(control_frame, image=next_btn_img, borderwidth=0, command=next_song)
play_button = Button(control_frame, image=play_btn_img, borderwidth=0, command=play)
pause_button = Button(control_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused))
stop_button = Button(control_frame, image=stop_btn_img, borderwidth=0, command=stop)

prev_button.grid(row=0,column=0,padx= 5)
next_button.grid(row=0,column=1,padx= 5)
play_button.grid(row=0,column=2,padx= 5)
pause_button.grid(row=0,column=3,padx= 5)
stop_button.grid(row=0,column=4,padx= 5)

# 4 On crée le menu principal
my_menu = Menu(root)
root.config(menu=my_menu)

#menu add song
add_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Ajouter", menu=add_song_menu)
add_song_menu.add_command(label="Ajouter un morceau", command=add_song)
add_song_menu.add_command(label="Ajouter plusieurs morceaux", command=add_many_songs)

#menu delete song
delete_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Enlever", menu=delete_song_menu)
delete_song_menu.add_command(label="Enlever un morceau", command=delete_song)
delete_song_menu.add_command(label="Enlever tous les morceaux", command=delete_all_songs)

# Création de la bar de status
status_bar = Label(root, text="Temps/Longueur morceau", bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X,side=BOTTOM, ipady=2)
# 5 Label temporaire qui va nous servir a ajouter les textes des morceaux
# my_label = Label(root, text="")
# my_label.pack(pady=10)






root.mainloop()