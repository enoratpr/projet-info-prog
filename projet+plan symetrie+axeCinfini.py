# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 10:17:41 2023

@author: maude
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Root window
root = tk.Tk()
root.title('Coordonnées de la molécule')
root.resizable(False, False)
root.geometry('500x80')

def open_mol_file():
    # file type
    filetypes = (
        ('text files', '*.mol'),
        ('All files', '*.*')
    )
    # show the open file dialog
    # définir le type de fichiers
    filetypes = (('text files', '*.mol'), ('All files', '*.*'))
    # afficher la boîte de dialogue d'ouverture de fichier
    fichier = fd.askopenfile(filetypes=filetypes)


    with open(fichier.name, 'r') as f:        
        content = f.readlines()
        line4 = content[3]
        data = line4.split(" ")
        data_ok = list(filter(None,data)) #j'utilise la fonction filter ici aussi pour que ça fonctionne à tous les coups

        nc = int(data_ok[0]) # Nombre coordonées
        nl = int(data_ok[1]) # Nombre liaisons 


        #print(nc," ",nl,"") #verif

        nc_fin = nc + 4
        nl_fin = nl + nc + 4
        #extraction des coordonnées
        coo = []
        for line in range(4,nc_fin):
            line_content = content[line].split(" ")
            line_content_ok = list(filter(None,line_content))
            coo_line = []
            coo_line.append(line_content_ok[0])
            coo_line.append(line_content_ok[1])
            coo_line.append(line_content_ok[2])
            coo.append(coo_line)
       # print(coo) #verif


        #extraction des atomes
        atom = []
        for line in range(4,nc_fin):
            line_content = content[line].split(" ")
            line_content_ok = list(filter(None,line_content))
            atom_line = []
            atom_line.append(line_content_ok[3])
            atom.append(atom_line[0])  
       # print(atom)


        #extraction des liaisons
        liaisons = []
        for line in range(nc_fin,nl_fin):
            line_content = content[line].split(" ")
            line_content_ok = list(filter(None,line_content))
            liaison_line = []
            liaison_line.append(line_content_ok[0])
            liaison_line.append(line_content_ok[1])
            liaison_line.append(line_content_ok[2])
            liaisons.append(liaison_line)
      #  print(liaisons)


        # Convertir les coordonnées en un tableau NumPy
        coordinates_array = np.array(coo, dtype=float)
        
        
  # Calculer le centre des atomes
        center = np.mean(coordinates_array, axis=0)
        # calcul de la translation nécessaire pour ramener le centre de masse à (0, 0, 0)
        translation = -center
        # translation des coordonnées
        translated_coordinates = coordinates_array + translation
        # vérification si la molécule possède un centre d'inversion
        has_inversion_center = True
        for coord in coordinates_array:
            inv_coord = -coord
            if not np.any((coordinates_array == inv_coord).all(axis=1)):
                has_inversion_center = False
                break
        if has_inversion_center:
            print("La molécule possède un centre d'inversion.")
        else:
            print("La molécule ne possède pas de centre d'inversion.")
            
            
        #une boîte cubique dans laquelle votre molécule se trouvera forcément en entier,
        #sans avoir de problème de liaison éclatée    
        x_min, y_min, z_min = np.min(coordinates_array, axis=0)
        x_max, y_max, z_max = np.max(coordinates_array, axis=0)
        
        # Trouver la plus grande valeur absolue parmi les valeurs min/max
        limit = max(abs(x_min), abs(x_max), abs(y_min), abs(y_max), abs(z_min), abs(z_max))
        # Multiplier par 1.1 ou 1.2 pour éviter de couper des atomes en deux sur la limite
        limit *= 1.2 
        
        # Créer une figure 3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlim([-limit, limit])
        ax.set_ylim([-limit, limit])
        ax.set_zlim([-limit, limit])
       
       #Couleur atome 
        letters = ['C', 'H', 'N', 'O', 'S', 'Cl']
        x1 = coordinates_array[:,0]
        y1 = coordinates_array[:,1]
        z1 = coordinates_array[:,2]
        colors = {'O': 'red', 'H': 'white', 'N': 'blue', 'C': 'black', \
                  'S': 'yellow', 'Cl': 'green'}
        size = {'O': 1000, 'H': 500, 'N': 1500, 'C': 2000, 'S' : 1000, 'Cl': 750}
        
        atom_color_list=[]
        
        for i, letters in enumerate(atom):
                ax.scatter(x1[i], y1[i], z1[i], color=colors[letters], marker='o', s=size[letters])
                atom_color_list.append((letters, colors[letters]))
        print(set(atom_color_list)) #permet à ce que la liste soit non redondante
        
          
        fig.set_facecolor('grey')
     
        
        #linéarité de la molécule 
        # initialiser une variable pour stocker si la molécule est linéaire ou non
        is_linear = False
        
        for i in range(len(coordinates_array)):
           for j in range(i+1, len(coordinates_array)):
        # calculer le produit scalaire entre les vecteurs i et j
            vi = coordinates_array[i] / (np.linalg.norm(coordinates_array[i]) + 1e-16) #le 1e-16 sert juste Ã  Ã©viter le cas oÃ¹ la norme serait nulle
            vj = coordinates_array[j] / (np.linalg.norm(coordinates_array[j]) + 1e-16) #mÃªme si normalement on l'a dÃ©jÃ  Ã©vitÃ© avec les continue plus haut
            vect = np.dot(vi, vj)
            #print(vect)
            
        # stocker le produit scalaire linéaire s'il est trouvé
            if abs(vect) == 1 or nc == 2:
                is_linear = True
                break
        
           if is_linear:  # sortir de la boucle externe si un produit scalaire linéaire 
            #a été trouvé
             break 
         
            # imprimer le résultat
        if is_linear:
            print("La molécule est linéaire ")
        else:
            print("La molécule n'est pas linéaire.")
            if nc > 2 : 
                # Molécule plane      
                
                # Calculer les vecteurs de liaison entre les atomes
                vectors_array = np.diff(coordinates_array, axis=0)
        
                # Calculer le vecteur normal à la molécule
                normal_vector = np.cross(vectors_array[0], vectors_array[1])
        
               
                # Vérifier que tous les vecteurs de liaison sont parallèles au vecteur normal
                
                is_planar = True
                tolerance = 1e-10
                for i in range(len(vectors_array)):
                    dot_product = np.dot(vectors_array[i], normal_vector)
                    if not np.isclose(dot_product, 0, atol=tolerance):
                        is_planar = False
                        break
                
            # Afficher le résultat
                if is_planar:
                    print("La molécule est plane.") 
                else:
                    print("La molécule n'est pas plane.")
            else :
                print("La molécule ne comporte que deux atomes, elle ne peut donc être plane")
        plt.show()
        
        #Centre de masse 
        # [:, 0] première colonne du tableau numpy de la liste de coordonnées
        # [:,0] correspond aux coordonnées en x
        # [:,1] correspond aux y 
        # [:,2] correspond aux z
        mean1 = np.mean(coordinates_array[:,0])
        mean2 = np.mean(coordinates_array[:,1])
        mean3 = np.mean(coordinates_array[:,2])
        x = mean1
        y = mean2
        z = mean3
        color = 'purple'
        ax.scatter(x, y, z, s=100, c=color, marker='o')
        plt.show()
      #  print(mean1, mean2, mean3)
        
        # Tracer les liaisons
        for liaison in liaisons:
            # Récupérer les indices des deux atomes liés
            atom1_connectivite = int(liaison[0]) - 1
            atom2_connectivite = int(liaison[1]) - 1
#on enlève le  chiffre correspondant aux types de liaisons 
            # Récupérer les coordonnées des deux atomes reliés entre eux
            atom1_coord = coordinates_array[atom1_connectivite]
            atom2_coord = coordinates_array[atom2_connectivite]
            #tracer des liaisons simples, doubles et triples
            bond_type = int(liaison[2]) #le 3 ème élément de la liste liaison
            
       
            if bond_type == 2 :
                ax.plot([atom1_coord[0], atom2_coord[0]], [atom1_coord[1]+0.05, \
                atom2_coord[1]+0.05], [atom1_coord[2], atom2_coord[2]], '-', \
                linewidth= 3, color="red")
                    
                ax.plot([atom1_coord[0], atom2_coord[0]], [atom1_coord[1]-0.05, \
                atom2_coord[1]-0.05], [atom1_coord[2],atom2_coord[2]], '-', linewidth= 3, color="red")
            
            
            elif bond_type == 3 :
                ax.plot([atom1_coord[0], atom2_coord[0]], [atom1_coord[1], \
                atom2_coord[1]], [atom1_coord[2], atom2_coord[2]], '-', \
                linewidth=3, color="red")
                    
                ax.plot([atom1_coord[0], atom2_coord[0]], [atom1_coord[1]-0.08, \
                atom2_coord[1]-0.08], [atom1_coord[2], atom2_coord[2]], '-', \
                linewidth=3, color="red") 

                ax.plot([atom1_coord[0], atom2_coord[0]], [atom1_coord[1]+0.08, \
                atom2_coord[1]+0.08], [atom1_coord[2], atom2_coord[2]], '-', \
                linewidth=3, color="red")


            else :
                ax.plot([atom1_coord[0], atom2_coord[0]], [atom1_coord[1], \
                atom2_coord[1]], [atom1_coord[2], atom2_coord[2]], '-', \
                linewidth=3, color="red")
        
        # BoolÃ©en indiquant s'il y a un plan de symÃ©trie pour chaque atome
        is_symmetric = [False] * len(coordinates_array)
        
        #Array de taille n x n rempli de False pour stocker quels plans sont des plans de symÃ©trie avec des paires de points
        is_symmetric_array = np.array([[False for i in range(len(coordinates_array))] for i in range(len(coordinates_array))])    
        #print(is_symmetric_array)
        
        # Si la molécule a seulement trois atomes, qu'elle est linéaire et qu'elle possède un centre d'inversion, on sort de la boucle et on retourne que la molécule possède des plans de symétrie
        if len(coordinates_array) == 3 and is_linear and has_inversion_center:
            print("La molécule possède des plans de symétrie")
            # Vérifier si la molécule a un axe C infini
            x1, y1, z1 = coordinates_array[0]
            x2, y2, z2 = coordinates_array[1]
            x3, y3, z3 = coordinates_array[2]

            if (x1 == x2 == x3) or (y1 == y2 == y3) or (z1 == z2 == z3):
                print("La molécule possède un axe C infini")

                # Déterminer l'ordre de l'axe C infini
                if x1 == x2 == x3:
                    order = 3
                elif y1 == y2 == y3:
                    order = 3
                elif z1 == z2 == z3:
                    order = 3
                elif (x1 == x2 and y1 == y2) or (x1 == x3 and y1 == y3) or (x2 == x3 and y2 == y3):
                    order = 2
                else:
                    order = 1

                print(f"L'ordre de l'axe C infini est {order}")
            return is_symmetric_array
        for i in range(len(coordinates_array)):
            if np.array_equal(coordinates_array[i],np.zeros(3)):
                continue #pour passer cette itération
            for j in range(i+1, len(coordinates_array)):
                if np.array_equal(coordinates_array[j],np.zeros(3)):
                    continue #pour passer cette itération
        
                # calculer le vecteur position entre les atomes i et j
                # calculer le produit scalaire
                vi = coordinates_array[i] / (np.linalg.norm(coordinates_array[i]) + 1e-16) #le 1e-16 sert juste Ã  Ã©viter le cas oÃ¹ la norme serait nulle
                vj = coordinates_array[j] / (np.linalg.norm(coordinates_array[j]) + 1e-16) #mÃªme si normalement on l'a dÃ©jÃ  Ã©vitÃ© avec les continue plus haut
                dot_product = np.dot(vi, vj)
                #print(i,j,dot_product)

                if abs(dot_product)<1.01 and abs(dot_product)>0.99:
                    #print(f"Atomes {i+1} et {j+1} sont alignÃ©s avec le centre de masse.")
                    break  # Passer Ã  l'atome suivant
                else:
                    # Calcul du produit vectoriel et normalisation du vecteur rÃ©sultant
                    cross_prod = np.cross(coordinates_array[i], coordinates_array[j])
                    norm_cross_prod = cross_prod / np.linalg.norm(cross_prod)
                    B = norm_cross_prod #.tolist()
                    #print(B)
                    
                    # Calcul de la distance d entre le plan passant par le centre de masse et les deux atomes
                    d = np.dot(B,coordinates_array[i])
                    # Boucle sur tous les autres atomes de la molÃ©cule pour calculer le produit scalaire avec le vecteur normal B
                    refl = []
                    for k in range(len(coordinates_array)):
                        if k != i and k != j:
                            # Calcul du produit scalaire entre le vecteur position de A3 et le vecteur normal B
                            dot_prod_A3 = np.dot(coordinates_array[k], B)
                            #print(dot_prod_A3)
                            if dot_prod_A3 == 0:
                                #print(f"L'atome {k+1} est dans le plan des atomes {i+1} et {j+1}")
                                continue
                            A3_reflected = coordinates_array[k] - 2 * dot_prod_A3 * B
                    
                            # VÃ©rification si les coordonnÃ©es de la rÃ©flexion correspondent Ã  celles d'un autre atome
                            is_reflected = False
                    
                            for l in range(len(coordinates_array)):
                                if l != i and l != j and l != k:
                                    if np.allclose(coordinates_array[l], A3_reflected):
                                        # Les coordonnÃ©es de la rÃ©flexion correspondent Ã  celles d'un autre atome
                                        is_reflected = True
                                        #print(f"L'atome {l+1} correspond Ã  la rÃ©flexion de l'atome {k+1} par rapport au plan des atomes {i+1} et {j+1}")
                                        break
                                # Siles coordonnÃ©es de la rÃ©flexion correspondent Ã  celles d'un autre atome pour tous les atomes n'appartenant pas au plan,
                                # on a un plan de symÃ©trie pour l'atome A1 et on stocke le vecteur normal et la constante d du plan
                            if is_reflected:
                                is_symmetric[i] = True #pourtant is_reflected s'initialise Ã  False, du coup lÃ  on teste s'il est restÃ© Ã  False
                                refl.append(True)
                                break
                            else:
                                refl.append(False)
                    print(refl)
                    if False in refl:
                        print(f"Le plan contenant l'origine et les atomes {i+1} et {j+1} n'est pas un plan de symÃ©trie de la molÃ©cule")
                    else:
                        print(f"Le plan contenant l'origine et les atomes {i+1} et {j+1} est un plan de symÃ©trie de la molÃ©cule")
                        is_symmetric_array[i][j]=True
                        print(i,j)
                    
                
        #print(is_symmetric)
        print(is_symmetric_array)        
        
        
            
        

        
                    
        
                
        
        plt.show()
        
# crée un bouton pour avoir accès à nos fichiers
open_button = ttk.Button(root, text='Open a File', command=open_mol_file)
#position et taille du bouton open a file
open_button.grid(column=0, row=1 , padx=10, pady=10)
root.mainloop()