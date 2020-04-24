import os
import time
import difflib

def create_snapshot(name,path):
    #this function will create the snapshot in local directory
    #containing the path and their time of creation separated by '->'
    #and save with an extension to be uniquely identified

    
    #name, path variables will be passed as parameters
    
    name = name + ".snpst"
    #name will be concatinated with .snpst for their extensions
    
    file1 = open(name,"w+")
    #file will be opened in write format 
    
    directory = path[path.rindex('\\')+1:]
    #directory will save the child name whose snapshot is created
    
    file1.write(directory+"\n")
    #writing into file1

    file1.write(path+" -> "+str(os.path.getmtime(path))+"\n")
    #writing path and modification time into file1
    
    for root, directories, filenames in os.walk(path):
        for directory in directories:
            n1 = os.path.join(root, directory)
            file1.write(n1+" -> "+str(os.path.getctime(n1))+"\n")

            #writing sub-path and modification time into file1
        for filename in filenames:
            n2 = os.path.join(root,filename)
            file1.write(n2+" -> "+str(os.path.getmtime(n2))+"\n")
            #writing sub-file and modification time into file1

    file1.close()
        
    
def show_all_snapshots():
    #this function will print the name of all the user created snapshot
    print("Snapshots are:")
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith('.snpst'):
                print(file)
                #will search for all files ending with .snpst recursively and print the names
    print('\n')

    

def show_given_snapshot(name):
    #this function will print the data containing the snapshot whose name is passed as parameter

    
    #name will be passed as parameter
    
    name += ".snpst"
    #extension is added to the variable
    
    file1 = open(name,"r")
    #file is opened in read mode
    
    reader = file1.read()
    reader1 = reader.split("\n")
    #reader1 will contain path and time which will be inserted in as a list
    
    reader2 = []
    for i in reader1:
        reader2.append(i.split(" -> "))
        #reader2 will contain path and time in the list separately 
        
    for i in range(1,len(reader2)-1):
        print(reader2[i][0]+" -> "+time.ctime(float(reader2[i][1])))
        #path and time will be printed stored in the snapshot
        
    file1.close()


def parentfinder(snapshot1,snapshot2,name1,name2):
    #4 parameters are passed: snapshot1,snapshot2,name1,name2
    #snapshot1 and snapshot 2 are the value of snapshots
    #name1 and name2 will be the name of both files
    #this function will tell which snapshot contain root and which contain child directories
    
    for i in range(len(snapshot1)):
       if(snapshot2[1][0] in snapshot1[i]):
           return snapshot1,snapshot2,name1,name2
    for i in range(len(snapshot2)):
        if(snapshot1[1][0] in snapshot2[i]):
            return snapshot2,snapshot1,name2,name1
    return 0,0,0,0
    #returning 0 if there is no similarity in 2 snapshots
    

def compare_snapshot(name1,name2):
    #2 parameters containing name without the extensions
    #this function will compare the 2 snapshots and call its sub-funtions
    #also, it will read the saved snapshots and convert it into list containing [path],[time] as nested list
    
    name1 = name1 + ".snpst"
    #adding extensions to the variable name1
    name2 = name2 + ".snpst"
    #adding extensions to the variable name2
    
    file1 = open(name1,"r")
    file2 = open(name2,"r")
    #opening both files for comparing in read mode
    
    ff1 = file1.read()
    ff2 = file2.read()
    #ff1, ff2 are the variables storing data of snapshots 
    
    ff1_temp = ff1.split("\n")
    ff2_temp = ff2.split("\n")
    #spiling the data files with "\n" and storing in list
    
    f1 = []
    f2 = []
    for i in ff1_temp:
        f1.append(i.split(" -> "))
    for i in ff2_temp:
        f2.append(i.split(" -> "))
    f1.remove([''])
    f2.remove([''])
    #removing unnecessary spaces which were entered while creating a snapshot and spliting the data as path and their time

    parent,child,parent_name,child_name=parentfinder(f1,f2,name1,name2)
    #parmeters are passed to parentfinder() functions which will return the parent dir, child dir and their file names
    if(parent==0):
        print("No similarity")
        #when their is no similarity i.e totally different snapshots that are compared
        

        
    else:
        divider(parent,child,parent_name,child_name)
        #when there is similarity in 2 snapshots they are further proceeded to clean the parent directory


def divider(parent,child,parent_name,child_name):
    #this function will only keep that part of parent directory which is needed for comparing and store it in "new_parent"
    new_parent = []
    for i in parent:
        if(child[1][0] in i[0]):
            new_parent.append(i)
            #appending data into new_parent which is needed for comparing

    del(child[0])
    #deleting child name from the snapshot, it wont be needed for comparision
    
    if(new_parent == child):
        print("No modifications")
        #Same Snapshot if both snapshots are identical in their path and time

    else:
        final(new_parent,child,parent_name,child_name)
        #if not same then new_parent,child,parent_name,child_name will be passed for final comparision



def final(parent,child,parent_name,child_name):

    #to compare snapshot files as per their creation time and deciding early_snapshot and later_snapshot
    if(os.path.getctime(parent_name) > os.path.getctime(child_name)):
        early_snapshot, later_snapshot = child_name, parent_name
    else:
        early_snapshot, later_snapshot = parent_name, child_name

    #adding items from a list(parent,child) to dictionary(parent_dict,child_dict)
    parent_dict = {}
    child_dict = {}
    for i in parent:
        parent_dict.__setitem__(i[0],i[1])
    for i in child:
        child_dict.__setitem__(i[0],i[1])

    #adding only file/directories name into list and skipping their modificatio time
    list1 = []
    list2 = []
    for item in parent_dict.keys():
        list1.append(item)

    for item in child_dict.keys():
        list2.append(item)



    added = []
    #This list will store file/directory names that have been newly added 

    removed = []
    #This list will store file/directory names that have been removed

    common_files = []
    #This list will store file/directory names that are common in both snapshots

    modified = []
    #This list will store file/directory names that have been modified since old snapshot


    #difflib.ndiff: '-': file/directory unique to sequence 1
    #difflib.ndiff: '+': file/directory unique to sequence 2
    #difflib.ndiff: ' ': file/directory common to both sequences
    #difflib.ndiff: '?': file/directory not present in either input sequence
    #appending into list as per their properties
    diff = difflib.ndiff('\n'.join(list1).splitlines(),'\n'.join(list2).splitlines())
    for l in diff:
        if l.startswith('-'):
            removed.append(l[1:])
        elif l.startswith('+'):
            added.append(l[1:])
        elif l.startswith('?'):
            pass
        else:
            common_files.append(l.strip())
    #comparing modified time of files that are present in both snapshots
    for files in common_files:
        if parent_dict[files]!=child_dict[files]:
            modified.append(files)

    #printing file/directory removed from current snapshot
    print(f"\nFiles/Directories removed from current snapshot: '{later_snapshot}' : ")
    for i in removed:
        print(i)

    #printing file/directory added in current snapshot
    print(f"\nFiles/Directories added in current snapshot '{later_snapshot}' : ")
    for i in added:
        print(i)

    #printing file/directory that are modified
    print("\nFiles/Directories modified: ")
    for i in modified:
        print(i)

    
    
    


#main window which the user will be interacted
if __name__ == '__main__':         
    while(True):
        print("\n\nSNAPSHOT TOOL")
        print("\nPress 1 for Creating a Snapshot\nPress 2 to Show all Snapshots\nPress 3 to Compare 2 Snapshots\nPress 4 to Exit\n")
        choice = int(input("Enter your choice:"))
        if(choice==1):
            name = input("Enter Name of Snapshot:")
            path = input("Enter Path:")

            #user choice will be passed in the create_snapshot() function as the name and path 
            try:
                create_snapshot(name,path)
            except:
                print("Error in Snapshot Creation")
            else:
                print("Snapshot created successfully!!!")


        elif(choice==2):
            try:
                show_all_snapshots()
                #show_all_snapshot() will print all the snapshots created so far
            except:
                print("Enter in printing the Snapshots")
            else:
            
                name = input("Enter Name of Snapshot to view:")
                #Enter the name from the list that will be shown
                #Note: Enter the name of the snapshots without the extensions

                try:
                    show_given_snapshot(name)
                    #selected Snapshot will be displayed
                except:
                    print("Error in printing selected Snapshot")
            

        elif(choice==3):
            show_all_snapshots()
            name1 = input("Enter Name of Snapshot 1:")
            name2 = input("Enter Name of Snapshot 2:")
            #Enter the name of snapshots you want to compare without the extension
            try:
                compare_snapshot(name1,name2)
                #compare_snapshot() function will be called and compare the 2 snapshots
            except:
                print("Error on comparing the Snapshots")

        
        elif(choice==4):
            break

        else:
            print("Invalid entry\nTry again")
            #program will exit on pressing any other key
