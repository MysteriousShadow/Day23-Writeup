def encrypt23(s):
    encrypted = s[0]
    for i in range(1, len(s)):
        encrypted += str(ord(s[i])-ord(s[i-1])) #The resulting integer is converted into STRING, NOT passed into chr().
    return encrypted

print(encrypt23("flag"))

from itertools import product

def str_insert(source_str, insert_str, pos):
    #https://stackoverflow.com/questions/4022827/insert-some-string-into-given-string-at-given-index
    return source_str[:pos] + insert_str + source_str[pos:]

def enumerate_groupings(group):
    """
    For a group with N number of elements, there are N-1 slots for dividers.
    Each slot either has or does not have a divider, therefore having 2 possibilites.
    The total number of possibilites becomes 2**(N-1)
    """
    leading_negative=False
    if group[0]=="-":
        leading_negative=True
        group=group[1:]

    inital_group=group
    groupings=[]
    for dividers in [''.join(p) for p in product('10', repeat=(len(group)-1))]:
        #https://stackoverflow.com/questions/30442808/create-list-of-binary-strings-python
        group=inital_group
        index_acc=0
        for i,divider in enumerate(dividers):
            if divider=="1":
                group=str_insert(group," ",i+1+index_acc)
                index_acc+=1

        if leading_negative:
            group="-"+group

        groupings.append(group)

    return groupings

def decrypt23(e):
    decrypted=[]
    groups=e[1:].split("-")
    for i in range(1,len(groups)):
        groups[i]="-"+groups[i]

    for grouping in list(product(*[enumerate_groupings(group) for group in groups])):
        decrypt=e[0]
        int_grouping=list(map(int,[n for n in " ".join(grouping).split(" ")])) #converts all the string numbers to int.
        for i in range(len(int_grouping)):
            plain_ord=ord(decrypt[i])+int_grouping[i]
            if plain_ord not in range(33,126+1): #Ditch results that are outside of the printable ASCII range.
                break
            decrypt+=chr(plain_ord)
        else:
            decrypted.append(decrypt) #only append qualified ones (the 'break' didn't happen)

    return decrypted

print(decrypt23("f6-11620-13-918-2469-11157-94-116-115"))