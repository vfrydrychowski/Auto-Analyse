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
from tkinterhtml import HtmlFrame
import webbrowser

global listel #liste contenant les labels des noms de fichiers csv
listel=[0,0,0]
global res
res=["User", "Style1", "Style2"] #pour les noms des courbes
global parser #pour le préfixe du parser
parser = "Parser"
tabfig = np.array([]) #tableau des graphes à afficher
contenantonglets = None
l4 = None

def recupere(strGlob, nom_frame):
	"""
    Permet de récupérer les fichiers d'analyse csv dans l'explorateur de documents. 
    Impossible de sélectionner autre chose qu'un fichier csv. Une fois les fichiers sélectionnés les boutons correspondants deviennent inutilisables et si les trois csv ont été sélectionnés le bouton pour lancer l'analyse devient visible.
    Args:
        strGlob:   Stocke le contenu du csv.
        nom_frame:   Nom de la frame contenant le bouton sélectionné.
    """

    #on place le chemin du fichier à côté du bouton correspondant
	if(nom_frame == 'Frame2_1') : #on pack les éléments pour changer le nom de la courbe1
		if(listel[0] == 0) : #si on a pas déjà choisi un fichier
			filename = fd.askopenfilename(title="Ouvrir le fichier", filetypes=[("csv", "*.csv")])
			globals()[strGlob] = pd.read_csv(filename, delim_whitespace=True, index_col='time')
			s = filename.split("/")
			listel[0] = LabelFrame(Frame2_1_a, padx=2, pady=2)
			nom1.pack(side=LEFT)
			e1.pack(side=LEFT)
			bouton_entry1.pack(side=LEFT)
			listel[0].pack(fill="both", side=LEFT, expand="no")
			Label(listel[0], text=s[-1]).pack(side=RIGHT)
			bouton_style1['state']=DISABLED #bouton grisé pour ne plus pouvoir rajouter de fichier

	elif(nom_frame == 'Frame2_2') : #courbe2
		if(listel[1] == 0) :
			filename = fd.askopenfilename(title="Ouvrir le fichier", filetypes=[("csv", "*.csv")])
			globals()[strGlob] = pd.read_csv(filename, delim_whitespace=True, index_col='time')
			s = filename.split("/")
			listel[1] = LabelFrame(Frame2_2_a, padx=5, pady=5)
			nom2.pack(side=LEFT)
			e2.pack(side=LEFT)
			bouton_entry2.pack(side=LEFT)
			listel[1].pack(fill="both", side=LEFT, expand="no")
			Label(listel[1], text=s[-1]).pack(side=RIGHT)
			bouton_style2['state']=DISABLED

	else : #courbe3
		if(listel[2] == 0) :
			filename = fd.askopenfilename(title="Ouvrir le fichier", filetypes=[("csv", "*.csv")])
			globals()[strGlob] = pd.read_csv(filename, delim_whitespace=True, index_col='time')
			s = filename.split("/")
			listel[2] = LabelFrame(Frame2_3_a, padx=5, pady=5)
			nom3.pack(side=LEFT)
			e3.pack(side=LEFT)
			bouton_entry3.pack(side=LEFT)
			listel[2].pack(fill="both", side=LEFT, expand="no")
			Label(listel[2], text=s[-1]).pack(side=RIGHT)
			bouton_csvAn['state']=DISABLED


	if(csvan is not None and csvdyn is not None and csvdef is not None) : #si on a choisi les 3 csv on peut lancer l'analyse
		bouton_lancerAnalyse.pack()


def getEntry(entry, nom_frame) : #récupérer les saisies utilisateur pour les noms de courbes et le préfixe de parsing
	"""
    Récupère les saisies utilisateur pour changer les noms des courbes et le préfixe de parsing.
    Args:
        entry:   L'entrée dont on veut récupérer la saisie.
        nom_frame:   Nom de la frame contenant l'entrée sélectionnée.
    """
	if(nom_frame == 'Frame2_1') :
		res[0] = entry.get()
	elif(nom_frame == 'Frame2_2') :
		res[1] = entry.get()
	elif(nom_frame == 'Frame2_3') :
		res[2] = entry.get()
	else :
		parser = entry.get()
	

def save(tab) :
	"""
    Permet de sauvegarder l'ensemble des graphes et des tableaux de données utilisés pour l'analyse. 
    La sauvegarde s'effectue dans le dossier de l'interface.
    Lorsque l'utilisateur a cliqué sur le bouton "Sauvegarder" une fenêtre pop-up apparaît pour signalé que l'enregistrement a bien été effectué.
    Args:
        tab:   Tableau de figures contenant tous les graphes à afficher.
    """
	for i in range(len(tab)) :
		for j in range(len(tab[0])) :
			tab[j][i].savefig("tab"+str(i)+"."+str(j)+".png")
	data1, data2, data3 = an.get_data()
	data1.to_csv('tableau_analyse.csv', index=False)
	data2.to_csv('tableau_style1.csv', index=False)
	data3.to_csv('tableau_style2.csv', index=False)
	callback("Enregistré avec succès") #message indiquant que l'enregistrement s'est bien passé

def callback(texte) :
	"""
    Permet d'afficher une fenêtre pop-up avec le message de notre choix passé en paramètre.
    Args:
        texte:   String contenant le message à afficher.
    """
	showinfo('', texte)

def graph(csvan, csvdyn, csvdef, res0, res1, res2, parser) :
	"""
    Permet d'afficher les graphes. En récupérant le tableau de figures renvoyé par la fonction plot_graph du fichier analyse puis en affichant dynamiquement les onglets et les graphes à l'intérieur en fonction de la taille du tableau.
    Affiche également les résultats de l'analyse.
    Args:
        csvan:   Contenu du fichier csv à analyser.
        csvdyn:   Contenu du fichier csv du style 1.
        csvdef:   Contenu du fichier csv du style 2.
        res0:   Nom de la courbe du fichier à analyser donnée par l'utilisateur, par défaut User.
        res1:   Nom de la courbe du style 1 donnée par l'utilisateur, par défaut Style1.
        res2:   Nom de la courbe du style 2 donnée par l'utilisateur, par défaut Style2.
        parser:   Nom du préfixe de parsing donné par l'utilisateur, par défaut Parser.
        
    """
	global tabfig
	global contenantonglets
	global l4 
	tabfig = np.array(an.plot_graph(csvan, csvdyn, csvdef, res0, res1, res2, parser)) #on récupère la liste de figures
	if(len(tabfig)!=0) :
		i,j = tabfig.shape

		contenantfigs = []
		longlets = []

		#afficher le score
		fonctionValentin = an.get_score(csvan, csvdyn, csvdef)
		l4 = LabelFrame(Frame1, text="Resultats", padx=20, pady=20)
		l4.pack(fill="both", expand="yes")
		#affichage des résultats pour chaque tronçon
		for z in range(0,len(fonctionValentin)) :
			if(fonctionValentin[z][0]<0):
				Label(l4, text="Tronçon "+str(z+1)+" : Style1").pack()
			elif(fonctionValentin[z][0]>0):
				Label(l4, text="Tronçon "+str(z+1)+" : Style2").pack()
		scoreglobal=an.get_score_global(fonctionValentin,[1]*len(fonctionValentin))
		if(scoreglobal<0):	
			Label(l4, text="Résultat global : Style1").pack()
		else:
			Label(l4, text="Résultat global : Style2").pack()

		#on affiche les onglets dynamiquement
		contenantonglets = Frame(fenetre, borderwidth=2)
		contenantonglets.pack(side=TOP, padx=5, pady=5, expand=1, fill="both")
		onglets = ttk.Notebook(contenantonglets)

		#affichage des graphes sur les tronçons
		for k in range(i) :
			longlets.append(ttk.Frame(onglets))
			onglets.add(longlets[k], text="Tronçon" + str(k+1))

			contenantfigs.append(Canvas(longlets[k], highlightthickness=0, height=50, width=50))
			#contenantfigs[k].configure(highlightthickness=0)
			contenantfigs[k].pack(padx=2, pady=2, expand=1, fill="both")

			for l in range(j) :
				#créer des labels pour contenir les fig
				canvas = FigureCanvasTkAgg(tabfig[k][l], master=contenantfigs[k])
				canvas.draw()
				canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
				#a verifier si ça marche qd plusieurs tabs par onglets

		onglets.pack(side=BOTTOM, expand=1, fill="both")
		global saveButton
		saveButton = Button(fenetre, text="Sauvegarder", command=lambda: save(tabfig))
		saveButton.pack(side=BOTTOM)
		#bouton lancer analyse supprimé tant que les csv ne sont pas chargés et qu'on n'a pas réinit
		bouton_lancerAnalyse.pack_forget()
		#on peut modifier les poids
		boutonpoids.pack(side=TOP)

		fenetre.update()


def reinit(tab, frame, frame2) : #tout réinitialiser
	"""
    Permet de réinitialiser la fenêtre en supprimant le tableau de figures, les frames qui affichent les graphes et les résultats, ainsi que les éléments pour changer les noms des courbes.
    Supprime également les chemins affichés des csv sélectionnés, cache le bouton pour changer les poids et rend à nouveau utilisables les boutons pour choisir les csv.
    Args:
        tab:   Tableau de figures.
        frame:   Frame contenant les graphes.
        frame2:   Frame contenant les résultats.
    """
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
	bouton_entry1.pack_forget()
	nom1.pack_forget()
	e1.pack_forget()

	bouton_entry2.pack_forget()
	nom2.pack_forget()
	e2.pack_forget()

	bouton_entry3.pack_forget()
	nom3.pack_forget()
	e3.pack_forget()

	#on supprime le nom des csv
	global listel
	for i in range(len(listel)) :
		if(listel[i]!=0) :
			listel[i].destroy()
	listel=[0,0,0]

	#on enlève le bouton pour changer les poids
	boutonpoids.pack_forget()

	#on supprime le bouton de sauvegarde
	saveButton.pack_forget()

	#on rend à nouveau les boutons de choix de csv accessibles
	bouton_style1['state']=NORMAL
	bouton_style2['state']=NORMAL
	bouton_csvAn['state']=NORMAL

	#on met à jour la fenêtre
	fenetre.update()

entreevit = ""
entreeacc = ""
listptroncons = []
v = 0
a = 0
l = []

def changerPoids() :
	"""
    Permet de changer les poids des tronçons et des paramètres. Crée une nouvelle fenêtre dans laquelle l'utilisateur peut saisir les nouvelles valeurs. Les valeurs par défaut sont toutes à 1 et si l'utilisateur rentre une valeur qui n'est pas entre 0 et 1, celles-ci est automatiquement remmise à 1.
    """
	global page
	page = Toplevel(fenetre) #on ouvre une nouvelle page
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


def valider() : #valider les changements de poids
	"""
    Permet de valider les changements de poids, recalculer les résultats et les afficher. Ferme également la fenêtre de changement des poids.
    """
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
	#on supprime les anciens résultats et on en affiche des nouveaux
	l4.destroy()
	fonctionValentin = an.get_score(csvan, csvdyn, csvdef, float(a), float(v))
	resultglobal=an.get_score_global(fonctionValentin, l)

	l4 = LabelFrame(Frame1, text="Resultats", padx=20, pady=20)
	l4.pack(fill="both", expand="yes")
	#affichage des résultats pour chaque tronçon
	for z in range(0,len(fonctionValentin)) :
		if(fonctionValentin[z][0]<0):
			Label(l4, text="Tronçon "+str(z+1)+" : Style1").pack()
		elif(fonctionValentin[z][0]>0):
			Label(l4, text="Tronçon "+str(z+1)+" : Style2").pack()
	if(resultglobal<0):	
		Label(l4, text="Résultat global : Style1").pack()
	else:
		Label(l4, text="Résultat global : Style2").pack()
	page.destroy()


def affichedoc() :
	"""
    Ouvre la documentation dans le navigateur.
    """
	webbrowser.open('test.html')



#programme principal, créer la fenêtre et les boutons
fenetre = Tk()
fenetre.geometry("1080x720")

#création des frames
Frame1 = Frame(fenetre, borderwidth=2)
Frame1.pack(side=LEFT, padx=50, pady=50)

Frame2 = Frame(Frame1, borderwidth=2)
Frame2.pack(side=TOP, padx=5, pady=5)

Frame2_1 = Frame(Frame2, borderwidth=2)
Frame2_1.pack(padx=5, pady=5)
Frame2_1_a = Frame(Frame2_1, borderwidth=2)
Frame2_1_a.pack(side=TOP, padx=5, pady=5)
Frame2_1_b = Frame(Frame2_1, borderwidth=2)
Frame2_1_b.pack(side=BOTTOM, padx=5, pady=5)

Frame2_2 = Frame(Frame2, borderwidth=2)
Frame2_2.pack(padx=5, pady=5)
Frame2_2_a = Frame(Frame2_2, borderwidth=2)
Frame2_2_a.pack(side=TOP, padx=5, pady=5)
Frame2_2_b = Frame(Frame2_2, borderwidth=2)
Frame2_2_b.pack(side=BOTTOM, padx=5, pady=5)

Frame2_3 = Frame(Frame2, borderwidth=2)
Frame2_3.pack(padx=5, pady=5)
Frame2_3_a = Frame(Frame2_3, borderwidth=2)
Frame2_3_a.pack(side=TOP, padx=5, pady=5)
Frame2_3_b = Frame(Frame2_3, borderwidth=2)
Frame2_3_b.pack(side=BOTTOM, padx=5, pady=5)

Frame3 = Frame(Frame1, borderwidth=2)
Frame3.pack(padx=5, pady=5)

csvdyn = None 
bouton_style1 = Button(Frame2_1_a, text = "Style 1", state=NORMAL, command=lambda: recupere('csvdyn', 'Frame2_1'))
bouton_style1.pack(side=LEFT, padx=5, pady=5)

csvdef = None
bouton_style2 = Button(Frame2_2_a, text = "Style 2", state=NORMAL, command=lambda: recupere('csvdef', 'Frame2_2'))
bouton_style2.pack(side=LEFT, padx=5, pady=5)

csvan = None
bouton_csvAn = Button(Frame2_3_a, text = "Csv à analyser", state=NORMAL, command=lambda: recupere('csvan', 'Frame2_3'))
bouton_csvAn.pack(side=LEFT, padx=5, pady=5)

bouton_lancerAnalyse = Button(Frame1, text="Lancer l'analyse", command=lambda: graph(csvan, csvdyn, csvdef, res[0], res[1], res[2], parser))

bouton_reinit = Button(Frame1, text="Réinitialiser", command=lambda: reinit(tabfig, contenantonglets, l4))
bouton_reinit.pack() 

boutonpoids = Button(Frame1, text="Changer les poids", command=lambda: changerPoids())

boutondoc = Button(Frame2, text = "Documentation", command=affichedoc)
boutondoc.pack()

global saveButton

#changer nom courbe
string1 = None
nom1 = Label(Frame2_1_b, text='Nom de la courbe')
e1 = Entry(Frame2_1_b, textvariable=string1)
bouton_entry1 = Button(Frame2_1_b, text = "Valider", command=lambda: getEntry(e1, 'Frame2_1'))
string2 = None
nom2 = Label(Frame2_2, text='Nom de la courbe')
e2 = Entry(Frame2_2, textvariable=string2)
bouton_entry2 = Button(Frame2_2, text = "Valider", command=lambda: getEntry(e2, 'Frame2_2'))
string3 = None
nom3 = Label(Frame2_3, text='Nom de la courbe')
e3 = Entry(Frame2_3, textvariable=string3)
bouton_entry3 = Button(Frame2_3, text = "Valider", command=lambda: getEntry(e3, 'Frame2_3'))

#changer le préfixe du parser
nomp = Label(Frame2, text='Changer le préfixe de parsing')
nomp.pack(side=LEFT, padx=10, pady=10)
ep = Entry(Frame2, textvariable=string)
ep.pack(side=LEFT, padx=2, pady=2)
boutonparser = Button(Frame2, text = "Valider", command=lambda: getEntry(ep, Frame2))
boutonparser.pack(side=LEFT, padx=10, pady=10)

fenetre.mainloop()