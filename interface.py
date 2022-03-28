from tkinter import *
from tkinter import filedialog as fd
from tkinter.messagebox import *
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import string
import pandas as pd
import analyse as an
import numpy as np

def recupere(strGlob):
	filename = fd.askopenfilename(title="Ouvrir le fichier", filetypes=[("csv", "*.csv")])
	globals()[strGlob] = pd.read_csv(filename, delim_whitespace=True, index_col='time')
	

#def save(figure) :
	#fig.savefig(figure)

def graph(csvan, csvdyn, csvdef) :
	tabfig = np.array(an.plot_graph(csvan, csvdyn, csvdef))
	i,j = tabfig.shape
	contenantfigs = []

	longlets = []
	lbuttons = []
	contenantonglets = Frame(fenetre, borderwidth=2)
	contenantonglets.pack(side=RIGHT, padx=50, pady=50)
	onglets = ttk.Notebook(contenantonglets)

	for k in range(i) :
		longlets.append(ttk.Frame(onglets))
		onglets.add(longlets[k], text="Tronçon" + str(k+1))
		lbuttons.append(Button(longlets[k], text="Sauvegarder"))
		lbuttons[k].pack(side=BOTTOM)

		contenantfigs.append(Frame(longlets[k], borderwidth=2))
		contenantfigs[k].pack(padx=10, pady=10)
		for l in range(j) :
			#créer des labels pour contenir les fig
			canvas = FigureCanvasTkAgg(tabfig[k][l], master=contenantfigs[k])
			canvas.draw()
			canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
			#a verifier si ça marche qd plusieurs tabs par onglets

	onglets.pack(side=BOTTOM, expand=1, fill="both")


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

Frame1 = Frame(fenetre, borderwidth=2)
Frame1.pack(side=LEFT, padx=50, pady=50)

Frame2 = Frame(Frame1, borderwidth=2)
Frame2.pack(side=TOP, padx=5, pady=5)

Label(Frame2, text="CSV").pack(side=TOP, padx=5, pady=5)

Frame3 = Frame(Frame1, borderwidth=2)
Frame3.pack(padx=5, pady=5)

Label(Frame3, text="Paramètres").pack(side=TOP, padx=5, pady=5)

csvdyn = None 
bouton = Button(Frame2, text = "Csv dynamique", command=lambda: recupere('csvdyn'))
bouton.pack(side=TOP, padx=5, pady=5)
#print(csvdyn)

csvdef = None
bouton1 = Button(Frame2, text = "Csv défensif", command=lambda: recupere('csvdef'))
bouton1.pack(padx=5, pady=5)

csvan = None
bouton2 = Button(Frame2, text = "Csv à analyser", command=lambda: recupere('csvan'))
bouton2.pack(padx=5, pady=5)

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

fenetre.mainloop()