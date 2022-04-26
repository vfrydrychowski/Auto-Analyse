from tkinter import *
from tkinter import filedialog as fd
from tkinter.messagebox import *
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt
import string
import pandas as pd
import analyse as an
import numpy as np
#from tkinterhtml import HtmlFrame

global listel #liste contenant les labels des noms de fichiers csv
listel=[]
global res
res=["User", "Style1", "Style2"]
global parser
parser = "Parser"
tabfig = np.array([])
contenantonglets = None
l4 = None

def recupere(strGlob, nom_frame): #pour aller récupérer les csv, impossible de prendre un autre type de fichier
	filename = fd.askopenfilename(title="Ouvrir le fichier", filetypes=[("csv", "*.csv")])
	globals()[strGlob] = pd.read_csv(filename, delim_whitespace=True, index_col='time')
	s = filename.split("/")

	#on place notre label à côté du bouton correspondant
	string2=None
	string3=None
	if(nom_frame == 'Frame2_1') : #on pack les éléments pour changer nom courbe1
		listel.append(LabelFrame(Frame2_1, padx=2, pady=2))
		nom1.pack(side=TOP)
		e1.pack(side=TOP)
		boutone1.pack(side=TOP)

	elif(nom_frame == 'Frame2_2') : #courbe2
		listel.append(LabelFrame(Frame2_2, padx=5, pady=5))
		nom2.pack(side=TOP)
		e2.pack(side=TOP)
		boutone2.pack(side=TOP)

	else : #courbe3
		listel.append(LabelFrame(Frame2_3, padx=5, pady=5))
		nom3.pack(side=TOP)
		e3.pack(side=TOP)
		boutone3.pack(side=TOP)

	listel[-1].pack(fill="both", side=LEFT, expand="no")
	Label(listel[-1], text=s[-1]).pack(side=RIGHT)

	if(csvan is not None and csvdyn is not None and csvdef is not None) :
		bouton9.pack()


def getEntry(entry, nom_frame) :
	if(nom_frame == 'Frame2_1') :
		res[0] = entry.get()
	elif(nom_frame == 'Frame2_2') :
		res[1] = entry.get()
	elif(nom_frame == 'Frame2_3') :
		res[2] = entry.get()
	else :
		parser = entry.get()
	

def save(tab) : #sauvegarder les graphes
	for i in range(len(tab)) :
		for j in range(len(tab[0])) :
			tab[j][i].savefig("tab"+str(i)+"."+str(j)+".png")

def graph(csvan, csvdyn, csvdef, res0, res1, res2, parser) :
	print("a" + res0)
	#on récupère la liste de figures
	global tabfig
	global contenantonglets
	global l4 
	tabfig = np.array(an.plot_graph(csvan, csvdyn, csvdef, res0, res1, res2, parser))
	i,j = tabfig.shape

	contenantfigs = []
	longlets = []
	lbuttons = []

	#on affiche les onglets dynamiquement
	
	fonctionValentin = an.get_score(csvan, csvdyn, csvdef)
	l4 = LabelFrame(Frame1, text="Resultats", padx=20, pady=20)
	l4.pack(fill="both", expand="yes")
	#affichage des résultats pour chaque tronçon
	for z in range(0,len(fonctionValentin)) :
		if(fonctionValentin[z][0]<0):
			Label(l4, text="Tronçon "+str(z+1)+" : Style1").pack()
		elif(fonctionValentin[z][0]>0):
			Label(l4, text="Tronçon "+str(z+1)+" : Style2").pack()
		
	contenantonglets = Frame(fenetre, borderwidth=2)
	contenantonglets.pack(side=TOP, padx=5, pady=5)
	onglets = ttk.Notebook(contenantonglets)

	#affichage des graphes sur les tronçons
	for k in range(i) :
		longlets.append(ttk.Frame(onglets))
		onglets.add(longlets[k], text="Tronçon" + str(k+1))

		contenantfigs.append(Canvas(longlets[k], borderwidth=2))
		contenantfigs[k].pack(padx=2, pady=2)

		lbuttons.append(Button(longlets[k], text="Sauvegarder", command=lambda: save(tabfig)))
		lbuttons[k].pack(side=BOTTOM)
		for l in range(j) :
			#créer des labels pour contenir les fig
			canvas = FigureCanvasTkAgg(tabfig[k][l], master=contenantfigs[k])
			canvas.draw()
			canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
			#a verifier si ça marche qd plusieurs tabs par onglets

	onglets.pack(side=BOTTOM, expand=1, fill="both")

	#bouton lancer analyse supprimé tant que les csv ne sont pas chargés et qu'on n'a pas réinit
	bouton9.pack_forget()

	fenetre.update()


def reinit(tab, frame, frame2) :
#si le tab n'est pas vide c'est qu'on a un affichage donc on le supprime
	if(tab.ndim and tab.size) :
		#on supprime la frame qui les affiche
		frame.destroy()
		#onsupprime le résultat
		frame2.destroy()

	#on supprime le contenu du tableau de figures
	for i in range(tab.shape[0]) :
		for j in range(tab.shape[1]) :
			tab[i][j].clf()


#on enlève les cases pour les noms de courbes
	boutone1.pack_forget()
	nom1.pack_forget()
	e1.pack_forget()

	boutone2.pack_forget()
	nom2.pack_forget()
	e2.pack_forget()

	boutone3.pack_forget()
	nom3.pack_forget()
	e3.pack_forget()
	#on supprime le nom des csv
	for i in range(len(listel)) :
		listel[i].destroy()
	#on met à jour la fenêtre
	fenetre.update()

entreevit = ""
entreeacc = ""
listptroncons = []
v = 0
a = 0
l = []

def changerPoids() :
	global page
	page = Toplevel(fenetre)
	global entreevit, entreeacc, listptroncons
	vit = StringVar()
	vit.set("1")
	nomv = Label(page, text='Poids vitesse')
	nomv.pack(side=TOP, padx=10, pady=10)
	entreevit = Entry(page, textvariable=vit, width=20)
	entreevit.pack()
	acc = StringVar()
	acc.set("1")
	noma = Label(page, text='Poids accélérations')
	noma.pack(side=TOP, padx=10, pady=10)
	entreeacc = Entry(page, textvariable=acc, width=20)
	entreeacc.pack()
	listptroncons = []
	for i in range(tabfig.shape[0]) :
		value = StringVar()
		value.set("1")
		nomval = Label(page, text='Poids tronçon'+str(i+1))
		nomval.pack(side=TOP, padx=10, pady=10)
		entree = Entry(page, textvariable=value, width=20)
		entree.pack()
		listptroncons.append(entree)

	bouton = Button(page, text = "Valider", command=lambda: valider())
	bouton.pack(side=BOTTOM, padx=5, pady=5)


def valider() :
	global v, a, l
	#si l'user a mis une val qui n'est pas entre 0 et 1 on remet tout à 1
	v = entreevit.get()
	if(float(v)<0 or float(v)>1) :
		v = 1
	if(float(a)<0 or float(a)>1) :
		a = 1
	a = entreeacc.get()
	for i in range(tabfig.shape[0]) :
		if(float(listptroncons[i].get())<0 or float(listptroncons[i].get())>1) :
			l.append(1)
		else :
			l.append(float(listptroncons[i].get()))
	global l4
	l4.destroy()
	fonctionValentin = an.get_score(csvan, csvdyn, csvdef, float(a), float(v))
	resultglobal=an.get_score_global(fonctionValentin, l)
	l4 = LabelFrame(Frame1, text="Resultats", padx=20, pady=20)
	l4.pack(fill="both", expand="yes")
	#affichage des résultats pour chaque tronçon
	for z in range(0,len(fonctionValentin)) :
		if(fonctionValentin[z][0]<0):
			Label(l4, text="Tronçon "+str(z)+" : Style1").pack()
		elif(fonctionValentin[z][0]>0):
			Label(l4, text="Tronçon "+str(z)+" : Style2").pack()
	Label(l4, text="Résultat global : "+str(resultglobal))
	page.destroy()


fenetre = Tk()
fenetre.geometry("900x600")

#création des frames

Frame1 = Frame(fenetre, borderwidth=2)
Frame1.pack(side=LEFT, padx=50, pady=50)

Frame2 = Frame(Frame1, borderwidth=2)
Frame2.pack(side=TOP, padx=5, pady=5)

Frame2_1 = Frame(Frame2, borderwidth=2)
Frame2_1.pack(padx=5, pady=5)

Frame2_2 = Frame(Frame2, borderwidth=2)
Frame2_2.pack(padx=5, pady=5)

Frame2_3 = Frame(Frame2, borderwidth=2)
Frame2_3.pack(padx=5, pady=5)

Frame3 = Frame(Frame1, borderwidth=2)
Frame3.pack(padx=5, pady=5)

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

bouton9 = Button(Frame1, text="Lancer l'analyse", command=lambda: graph(csvan, csvdyn, csvdef, res[0], res[1], res[2], parser))

bouton10 = Button(Frame1, text="Réinitialiser", command=lambda: reinit(tabfig, contenantonglets, l4))
bouton10.pack() 

#changer nom courbe
string1 = None
nom1 = Label(Frame2_1, text='Nom de la courbe')
e1 = Entry(Frame2_1, textvariable=string1)
boutone1 = Button(Frame2_1, text = "Valider", command=lambda: getEntry(e1, 'Frame2_1'))
string2 = None
nom2 = Label(Frame2_2, text='Nom de la courbe')
e2 = Entry(Frame2_2, textvariable=string2)
boutone2 = Button(Frame2_2, text = "Valider", command=lambda: getEntry(e2, 'Frame2_2'))
string3 = None
nom3 = Label(Frame2_3, text='Nom de la courbe')
e3 = Entry(Frame2_3, textvariable=string3)
boutone3 = Button(Frame2_3, text = "Valider", command=lambda: getEntry(e3, 'Frame2_3'))

#changer le préfixe du parser
nomp = Label(Frame2, text='Changer le préfixe de parsing')
nomp.pack(side=TOP, padx=10, pady=10)
ep = Entry(Frame2, textvariable=string)
ep.pack(side=TOP, padx=2, pady=2)
boutonep = Button(Frame2, text = "Valider", command=lambda: getEntry(ep, Frame2))
boutonep.pack(side=TOP, padx=10, pady=10)

boutonpoids = Button(Frame2, text="Changer les poids", command=lambda: changerPoids())
boutonpoids.pack()

fenetre.mainloop()