import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

# Root window
root = tk.Tk()
root.title('coordonnées de la molécule')
root.resizable(False, False)
root.geometry('550x250')

# Text editor
text = tk.Text(root, height=12)
text.grid(column=0, row=0, sticky='nsew')


def open_mol_file():
    # file type
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.mol')
    )
    # show the open file dialog
    f = fd.askopenfile(filetypes=filetypes)
    # read the text file and show its content on the Text
    line=f.read()
    print(line)
    f.close()

# open file button
open_button = ttk.Button(
    root,
    text='Open a File',
    command=open_mol_file
)
#position et taille du bouton open a file
open_button.grid(column=0, row=1, sticky='w', padx=10, pady=10)


root.mainloop()




