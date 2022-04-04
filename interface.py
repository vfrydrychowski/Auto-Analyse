from tkinter import *
from tkinter import filedialog as fd
from tkinter.messagebox import *
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot
import string
import pandas as pd
import analyse as an
import numpy as np
from PIL import Image

global listel #liste contenant les labels des noms de fichiers csv
listel=[]

def recupere(strGlob, nom_frame): #pour aller récupérer les csv, impossible de prendre un autre type de fichier
	filename = fd.askopenfilename(title="Ouvrir le fichier", filetypes=[("csv", "*.csv")])
	globals()[strGlob] = pd.read_csv(filename, delim_whitespace=True, index_col='time')
	s = filename.split("/")

	#on place notre label à côté du bouton correspondant
	if(nom_frame == 'Frame2_1') :
		listel.append(LabelFrame(Frame2_1, padx=5, pady=5))
	elif(nom_frame == 'Frame2_2') :
		listel.append(LabelFrame(Frame2_2, padx=5, pady=5))
	else :
		listel.append(LabelFrame(Frame2_3, padx=5, pady=5))

	listel[-1].pack(fill="both", side="right", expand="no")
	Label(listel[-1], text=s[-1]).pack()
	

def save(canvas, filename) :
	canvas.postscript(file = filename+'.eps')
	img = Image.open(filename+'.eps')
	img.save(filename+'.png', 'png')

def graph(csvan, csvdyn, csvdef) :

	#on récupère la liste de figures
	global tabfig
	tabfig = np.array(an.plot_graph(csvan, csvdyn, csvdef))
	i,j = tabfig.shape

	#global contenantfigs
	contenantfigs = []

	longlets = []
	lbuttons = []
	#on affiche les onglets dynamiquement

	global contenantonglets
	global Frame4
	
	fonctionValentin = 0
	Frame4 = Frame(fenetre, borderwidth=2)
	Frame4.pack(side=BOTTOM, padx=5, pady=5)
	l4 = LabelFrame(Frame4, text="Resultats", padx=20, pady=20)
	l4.pack(fill="both", expand="yes")
	if(fonctionValentin==0):
		Label(l4, text="Style1").pack()
	else:
		Label(l4, text="Style2").pack()
		
	contenantonglets = Frame(Frame4, borderwidth=2)
	contenantonglets.pack(side=TOP, padx=50, pady=50)
	onglets = ttk.Notebook(contenantonglets)


	for k in range(i) :
		longlets.append(ttk.Frame(onglets))
		onglets.add(longlets[k], text="Tronçon" + str(k+1))

		contenantfigs.append(Canvas(longlets[k], borderwidth=2))
		contenantfigs[k].pack(padx=10, pady=10)
		lbuttons.append(Button(longlets[k], text="Sauvegarder", command=lambda: save(contenantfigs[k], "graph"+str(k))))
		lbuttons[k].pack(side=BOTTOM)
		for l in range(j) :
			#créer des labels pour contenir les fig
			canvas = FigureCanvasTkAgg(tabfig[k][l], master=contenantfigs[k])
			canvas.draw()
			canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
			#a verifier si ça marche qd plusieurs tabs par onglets

	onglets.pack(side=BOTTOM, expand=1, fill="both")

	fenetre.update()


def reinit(tab, frame, frame2) :
	#on supprime le contenu du tableau de figures
	for i in range(tab.shape[0]) :
		for j in range(tab.shape[1]) :
			tab[i][j].clf()

	#on supprime la frame qui les affiche
	frame.destroy()
	#onsupprime le résultat
	frame2.destroy()

	#on supprime le nom des csv
	for i in range(len(listel)) :
		listel[i].destroy()

	#on met à jour la fenêtre
	fenetre.update()


fenetre = Tk()
fenetre.geometry("900x600")

#Canvas(fenetre, width=250, height=100, bg='white').pack(side=TOP, padx=5, pady=5)

#l = LabelFrame(fenetre, text="Documentation", bg='ivory', fg='black', padx=20, pady=20)
#l.pack(side=BOTTOM, fill="both", expand="yes")
#l2 = Label(l, text=content, bg='ivory', fg='black').pack(side=BOTTOM, padx=10, pady=10)

#scroll_bar = Scrollbar(l)
#scroll_bar.pack(side=RIGHT, fill=Y)

#text = Text(l, yscrollcommand=scroll_bar.set, bg='ivory', fg='black', height=10, width=10)
#text.insert(INSERT, content)
#text.pack()

#scroll_bar.config(command=text.yview)

#contenantonglets = Frame(fenetre, borderwidth=2)

Frame1 = Frame(fenetre, borderwidth=2)
Frame1.pack(side=LEFT, padx=50, pady=50)

Frame2 = Frame(Frame1, borderwidth=2)
Frame2.pack(side=TOP, padx=5, pady=5)

Label(Frame2, text="CSV").pack(side=TOP, padx=5, pady=5)

Frame2_1 = Frame(Frame2, borderwidth=2)
Frame2_1.pack(padx=5, pady=5)

Frame2_2 = Frame(Frame2, borderwidth=2)
Frame2_2.pack(padx=5, pady=5)

Frame2_3 = Frame(Frame2, borderwidth=2)
Frame2_3.pack(padx=5, pady=5)

Frame3 = Frame(Frame1, borderwidth=2)
Frame3.pack(padx=5, pady=5)

Label(Frame3, text="Paramètres").pack(side=TOP, padx=5, pady=5)

csvdyn = None 
bouton = Button(Frame2_1, text = "Style 1", command=lambda: recupere('csvdyn', 'Frame2_1'))
bouton.pack(side=LEFT, padx=5, pady=5)
#print(csvdyn)

csvdef = None
bouton1 = Button(Frame2_2, text = "Style 2", command=lambda: recupere('csvdef', 'Frame2_2'))
bouton1.pack(side=LEFT, padx=5, pady=5)

csvan = None
bouton2 = Button(Frame2_3, text = "Csv à analyser", command=lambda: recupere('csvan', 'Frame2_3'))
bouton2.pack(side=LEFT, padx=5, pady=5)

bouton3 = Checkbutton(Frame3, text="vitesse")
bouton3.pack()

bouton4 = Checkbutton(Frame3, text="accélération")
bouton4.pack()

bouton5 = Checkbutton(Frame3, text="_____")
bouton5.pack()

bouton6 = Checkbutton(Frame3, text="_____")
bouton6.pack()

bouton7 = Checkbutton(Frame3, text="_____")
bouton7.pack()

bouton8 = Checkbutton(Frame3, text="_____")
bouton8.pack()

bouton9 = Button(Frame1, text="Lancer l'analyse", command=lambda: graph(csvan, csvdyn, csvdef))
bouton9.pack()

bouton10 = Button(Frame1, text="Réinitialiser", command=lambda: reinit(tabfig, contenantonglets, Frame4))
bouton10.pack()


fenetre.mainloop()