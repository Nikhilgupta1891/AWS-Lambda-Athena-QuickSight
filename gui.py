import boto3
import boto.s3
import sys
from boto.s3.key import Key
from tkinter import *
from tkinter.filedialog import askopenfilename

master = Tk()
master.title('Athena DB Importer')

Label(master, text="Select and rename file to upload", font="Helvetica 16 underline").grid(row=0, columnspan=3)
Label(master, text="File Name").grid(row=1, column=0)
Label(master, text="File to Upload").grid(row=2, column=0)

fileNameField = Entry(master)
fileNameField.grid(row=1, column=1, columnspan=2)

selectedFileField = Entry(master, state=DISABLED)
selectedFileField.grid(row=2, column=1, columnspan=2)

def submitForm():
    desired_filename = fileNameField.get()

    if desired_filename == '':
        desired_filename = selectedFileField.get()
    else:
        desired_filename += '.csv'

    stripped_filename = desired_filename.split('/')[-1]
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(selectedFileField.get(), 'cerner-shipit', 'data/' + stripped_filename)

def chooseFile():
    filename = askopenfilename(parent=master)

    if filename != None and filename != '':
        selectedFileField.config(state=NORMAL)
        selectedFileField.delete(0, END)
        selectedFileField.insert(0, filename)
        selectedFileField.config(state=DISABLED)

Button(master, text='Select CSV', command=chooseFile).grid(row=3, column=1)
Button(master, text='Upload File', command=submitForm).grid(row=3, column=2)

mainloop( )
