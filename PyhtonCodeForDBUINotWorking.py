import boto3
import boto.s3
import sys

from boto.s3.key import Key
from tkinter import *
from tkinter.filedialog import askopenfilename

master = Tk()
master.title('Athena DB Importer')

def chooseFile():
    filename = askopenfilename(parent=master)

    if filename != None and filename != '':
        uploadFile(filename)

def uploadFile(filename):
    stripped_filename = filename.split('/')[-1]
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(filename, 'cerner-shipit', 'data/' + stripped_filename)

Label(master, text="Select and rename file to upload", font="Helvetica 16 underline").grid(row=0, columnspan=2)

Label(master, text="Enter Database Name").grid(row=1)
Label(master, text="DB username").grid(row=2)
Label(master, text="DB password").grid(row=3)
Label(master, text="Select Query").grid(row=4)

e1 = Entry(master)
e2 = Entry(master)
e3 = Entry(master)
e4 = Entry(master)

e1.grid(row=1, column=1)
e2.grid(row=2, column=1)
e3.grid(row=3, column=1)

Button(master, text='Select Query', command=chooseFile).grid(row=4, column=1, columnspan=2)

mainloop( )
