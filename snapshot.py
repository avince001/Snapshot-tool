import os
import time

def create_snapshot(name,path):
    
    #name, path variables will be passed as parameters
    
    name = name + ".snpst"
    #name will be concatinated with .snpst for their extensions
    
    file1 = open(name,"w+")
    #file will be opened in write format 
    
    directory = path[path.rindex('\\')+1:]
    #directory will save the child name whose snapshot is created
    
    file1.write(directory+"\n")
    #writing into file1

    file1.write(path+" @# "+str(os.path.getmtime(path))+"\n")
    #writing path and modification time into file1
    
    for root, directories, filenames in os.walk(path):
        for directory in directories:
            n1 = os.path.join(root, directory)
            file1.write(n1+" @# "+str(os.path.getmtime(n1))+"\n")

            #writing sub-path and modification time into file1
        for filename in filenames:
            n2 = os.path.join(root,filename)
            file1.write(n2+" @# "+str(os.path.getmtime(n2))+"\n")
            #writing sub-file and modification time into file1

    file1.close()
        
    
def show_all_snapshots():
    print("Snapshots are:")
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith('.snpst'):
                print(file)
                #will search for all files ending with .snpst recursively and print the names

    

def show_given_snapshot(name):
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
        reader2.append(i.split(" @# "))
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
        f1.append(i.split(" @# "))
    for i in ff2_temp:
        f2.append(i.split(" @# "))
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
    #this function will only keep that part of parent directory which is needed for comparing and stored in "new_parent"
    new_parent = []
    for i in parent:
        if(child[1][0] in i[0]):
            new_parent.append(i)
            #appending data into new_parent which is needed for comparing

    del(child[0])
    #deleting child name from the snapshot, it wont be needed for comparision
    
    if(new_parent == child):
        print("Same Snapshot")
        #Same Snapshot if both snapshots are identical in their path and time

    else:
        final(new_parent,child,parent_name,child_name)
        #if not same then new_parent,child,parent_name,child_name will be passed for final comparision



def final(parent,child,parent_name,child_name):
    #parent snapshot is modified to be compared directly with child snapshot

    #for modification of files and folder
    for i in range(0,len(child)):
        for j in range(0,len(parent)):
            if(child[i][0] == parent[j][0]):
                if(child[i][1] > parent[j][1]):
                    print(child[i][0]+" is modified later in Snapshot: "+child_name)
                if(child[i][1] < parent[j][1]):
                   print(parent[j][0]+" is modified later in Snapshot: "+parent_name) 
    

    final_parent = list(i[0] for i in parent)
    final_child = list(i[0] for i in child)

    #if certain file is not present parent_name snapshot
    for i in final_child:
        if i not in final_parent:
            print(i+" is not present in Snapshot: "+parent_name)

    ##if certain file is not present parent_name snapshot
    for i in final_parent:
        if i not in final_child:
            print(i+" is not present in Snapshot: "+child_name)


    


#main window which the user will be interacted
            
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
        name1 = input("Enter Name of Snapshot 1:")
        name2 = input("Enter Name of Snapshot 2:")
        #Enter the name of snapshots you want to compare without the extension
        try:
            compare_snapshot(name1,name2)
            #compare_snapshot() function will be called and compare the 2 snapshots
        except:
            print("Error on comparing the Snapshots")


    else:
        break
        #program will exit on pressing any other key
