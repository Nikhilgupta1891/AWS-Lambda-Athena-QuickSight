import boto3
import boto.s3
import sys
from boto.s3.key import Key
from tkinter import *
from tkinter.filedialog import askopenfilename

master = Tk()
master.title('Athena DB Importer')

Label(master, text="Select and rename files to upload", font="Helvetica 16 underline").grid(row=0, columnspan=3)
Label(master, text="File Name").grid(row=1, column=0)
Label(master, text="File to Upload").grid(row=2, column=0)
Label(master, text="Schema Name").grid(row=3, column=0)
Label(master, text="Schema to Upload").grid(row=4, column=0)
Label(master, text="Query Name").grid(row=5, column=0)
Label(master, text="Query to Upload").grid(row=6, column=0)

# Table data fields declaration
fileNameField = Entry(master)
fileNameField.grid(row=1, column=1, columnspan=2)

selectedFileField = Entry(master, state=DISABLED)
selectedFileField.grid(row=2, column=1, columnspan=2)

# Schema data fields declaration
schemaNameField = Entry(master)
schemaNameField.grid(row=3, column=1, columnspan=2)

selectedSchemaField = Entry(master, state=DISABLED)
selectedSchemaField.grid(row=4, column=1, columnspan=2)

# Query data fields declaration
queryNameField = Entry(master)
queryNameField.grid(row=5, column=1, columnspan=2)

selectedQueryField = Entry(master, state=DISABLED)
selectedQueryField.grid(row=6, column=1, columnspan=2)

def chooseFile():
    #For Table data
    filename = askopenfilename(parent=master)

    if filename != None and filename != '':
        selectedFileField.config(state=NORMAL)
        selectedFileField.delete(0, END)
        selectedFileField.insert(0, filename)
        selectedFileField.config(state=DISABLED)

    #For Schema Data
    schemaname = askopenfilename(parent=master)

    if schemaname != None and schemaname != '':
        selectedSchemaField.config(state=NORMAL)
        selectedSchemaField.delete(0, END)
        selectedSchemaField.insert(0, schemaname)
        selectedSchemaField.config(state=DISABLED)

    # For Query Data
    queryname = askopenfilename(parent=master)

    if queryname != None and queryname != '':
        selectedQueryField.config(state=NORMAL)
        selectedQueryField.delete(0, END)
        selectedQueryField.insert(0, queryname)
        selectedQueryField.config(state=DISABLED)

def submitForm():
    #For Table Data
    
    desired_filename = fileNameField.get()
    setting = ''
    if desired_filename == '':
        desired_filename = selectedFileField.get()
    else:
        desired_filename += '.csv'
    stripped_filename = desired_filename.split('/')[-1]
    setting += 'data/' + stripped_filename + ' '
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(selectedFileField.get(), 'cerner-shipit', 'data/' + stripped_filename)

    #For Schema Data
    desired_schemaname = fileNameField.get()
    if desired_schemaname == '':
        desired_schemaname = selectedSchemaField.get()
    else:
        desired_schemaname += '.txt'
    stripped_schemaname = desired_schemaname.split('/')[-1]
    setting += 'schema/' + stripped_schemaname + ' '
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(selectedSchemaField.get(), 'cerner-shipit', 'schema/' + stripped_schemaname)

    # For Query Data
    desired_queryname = fileNameField.get()
    if desired_queryname == '':
        desired_queryname = selectedQueryField.get()
    else:
        desired_queryname += '.txt'
    stripped_queryname = desired_queryname.split('/')[-1]
    setting += 'query/' + stripped_queryname
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(selectedQueryField.get(), 'cerner-shipit', 'query/' + stripped_queryname)

    # For the configs
    with open("settings.txt", "w+") as text_file:
        text_file.write(setting)
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file('settings.txt', 'cerner-shipit', 'conf/settings.txt')

Button(master, text='Select Files', command=chooseFile).grid(row=7, column=1)
Button(master, text='Upload Files', command=submitForm).grid(row=7, column=2)

mainloop( )
