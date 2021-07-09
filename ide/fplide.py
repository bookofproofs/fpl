from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext
from tkinter import messagebox

global_path = ''

window = Tk()
window.minsize(800, 600)
window.title('Formal Proving Language IDE')
textEditor = scrolledtext.ScrolledText(window, undo=True)
textEditor.config(bg='#362f2e', fg='#d2ded1', insertbackground='white')
textEditor['font'] =  ('consolas', '12')
textEditor.pack(expand=True, fill="both")


style = ttk.Style(window)
style.configure('TNotebook', tabposition='wn')

tabControl = ttk.Notebook(window,heigh=70)
tabControl.config()

tabErrors = ttk.Frame(tabControl)
tabErrors.config()
tabSyntax = ttk.Frame(tabControl)
tabSyntax.config()
tabSemantics = ttk.Frame(tabControl)
tabSemantics.config()
tabOutput = ttk.Frame(tabControl)
tabOutput.config()

tabControl.add(tabErrors, text='Error List')
tabControl.add(tabSyntax, text='Syntax Browser')
tabControl.add(tabSemantics, text='Semantics Browser')
tabControl.add(tabOutput, text='Output')

tabControl.pack(expand=True, fill="both")


def build_fpl_code():
    code = textEditor.get('1.0', END)
    messagebox.showinfo("FPL", "Not implemented yet!")


def open_file():
    path = askopenfilename(filetypes=[('FPL Files', '*.fpl'), ('Python Files', '*.py')])
    with open(path, 'r') as file:
        code = file.read()
        textEditor.delete("1.0", END)
        textEditor.insert("1.0", code)
        global global_path
        global_path = path


def save_file():
    global global_path
    if global_path == '':
        return save_file_as()
    with open(global_path, 'w') as file:
        code = textEditor.get('1.0', END)
        file.write(code)

def save_file_as():
    path = asksaveasfilename(filetypes=[('FPL Files', '*.fpl'), ('Python Files', '*.py')], initialfile=global_path)
    with open(path, 'w') as file:
        code = textEditor.get('1.0', END)
        file.write(code)


menuBar = Menu(window)

fileBar = Menu(menuBar, tearoff=0)
fileBar.add_command(label='Open', command=open_file)
fileBar.add_command(label='Save', command=save_file)
fileBar.add_command(label='Save As', command=save_file_as)
fileBar.add_command(label='Exit', command=exit)
menuBar.add_cascade(label='File', menu=fileBar)

buildBar = Menu(menuBar, tearoff=0)
buildBar.add_command(label='Build', command=build_fpl_code)
menuBar.add_cascade(label='Build', menu=buildBar)

window.config(menu=menuBar)
window.mainloop()
