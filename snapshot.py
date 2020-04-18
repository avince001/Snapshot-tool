import os
import time

def create_snapshot(name,path):
    
    name = name + ".snpst"
    file1 = open(name,"w+")
    
    directory = path[path.rindex('\\')+1:]
    file1.write(directory+"\n")
    file1.write(path+" @# "+str(os.path.getmtime(path))+"\n")
    for root, directories, filenames in os.walk(path):
        for directory in directories:
            n1 = os.path.join(root, directory)
            file1.write(n1+" @# "+str(os.path.getmtime(n1))+"\n")
        for filename in filenames:
            n2 = os.path.join(root,filename)
            file1.write(n2+" @# "+str(os.path.getmtime(n2))+"\n")
    file1.close()
        
    
def show_all_snapshots():
    print("Snapshots are:")
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith('.snpst'):
                print(file)

    

def show_given_snapshot(name):
    name += ".snpst"
    file1 = open(name,"r")
    reader = file1.read()
    reader1 = reader.split("\n")
    reader2 = []
    for i in reader1:
        reader2.append(i.split(" @# "))
    for i in range(1,len(reader2)-1):
        print(reader2[i][0]+" -> "+time.ctime(float(reader2[i][1])))
    file1.close()

def parentfinder(snapshot1,snapshot2,name1,name2):
    for i in range(len(snapshot1)):
       if(snapshot2[1][0] in snapshot1[i]):
           return snapshot1,snapshot2,name1,name2
    for i in range(len(b)):
        if(snapshot1[1][0] in snapshot2[i]):
            return snapshot2,snapshot1,name2,name1
    return 0,0
    

def compare_snapshot(name1,name2):
    
    name1 = name1 + ".snpst"
    
    name2 = name2 + ".snpst"
    file1 = open(name1,"r")
    file2 = open(name2,"r")
    ff1 = file1.read()
    ff2 = file2.read()
    ff1_temp = ff1.split("\n")
    ff2_temp = ff2.split("\n")
    f1 = []
    f2 = []
    for i in ff1_temp:
        f1.append(i.split(" @# "))
    for i in ff2_temp:
        f2.append(i.split(" @# "))
    f1.remove([''])
    f2.remove([''])

    parent,child,parent_name,child_name=parentfinder(f1,f2,name1,name2)
    if(parent==0):
        print("No similarity")
        

        
    else:
        divider(parent,child,parent_name,child_name)



def divider(a,b,a_name,b_name):

    lst = []
    for i in a:
        if(b[1][0] in i[0]):
            lst.append(i)

    del(b[0])

    if(lst == b):
        print("Same Snapshot")

    else:
        final(lst,b,a_name,b_name)



def final(lst,b,lst_name,b_name):
    for i in range(0,len(b)):
        for j in range(0,len(lst)):
            if(b[i][0] == lst[j][0]):
                if(b[i][1] > lst[j][1]):
                    print(b[i][0]+" is modified later")
    

    new_lst = list(i[0] for i in lst)
    new_b = list(i[0] for i in b)

    for i in new_b:
        if i not in new_lst:
            print(i+" is not present in "+lst_name+" snapshot")

    for i in new_lst:
        if i not in new_b:
            print(i+" is not present in "+b_name+" snapshot")


    



while(True):
    print("\n\nSNAPSHOT TOOL")
    print("\nPress 1 for Creating a Snapshot\nPress 2 to Show all Snapshots\nPress 3 to Compare 2 Snapshots\nPress 4 to Exit\n")
    choice = int(input("Enter your choice:"))
    if(choice==1):
        name = input("Enter Name of Snapshot:")
        path = input("Enter Path:")
        create_snapshot(name,path)


    elif(choice==2):
        show_all_snapshots()
        name = input("Enter Name of Snapshot to view:")
        show_given_snapshot(name)
        

    elif(choice==3):
        name1 = input("Enter Name of Snapshot 1:")
        name2 = input("Enter Name of Snapshot 2:")
        compare_snapshot(name1,name2)


    else:
        break
