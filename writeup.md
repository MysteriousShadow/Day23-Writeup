<h1>Writeup for Day23 of DailyCTF by n4m3n1ck</h1>

<h2>Challenge:</h2>
Reverse This Function to get the flag:

```python
def encrypt23(s):
    encrypted = s[0]
    for i in range(1, len(s)):
        encrypted += str(ord(s[i])-ord(s[i-1]))
    return encrypted
```
Encrypted flag: 
<code>f6-11620-13-918-2469-11157-94-116-115</code>

## What the encryption is doing:
The first letter of the plaintext is set to also be the first letter of the ciphertext.
Then, each number in the ciphertext is the difference in ASCII value of the corresponding plaintext character and its previous character.

So, the ASCII value of the second character, <code>s[1]</code>, of the plaintext minus the ASCII value of the first character, <code>f</code>, of the plaintext equals <code>6</code>.

Therefore, <code>6+ord('f')</code> equals <code>ord(s[1])</code>, so <code>s[1]</code> is <code>chr(108)</code> which is <code>l</code> (lower case L).

To further see this, we can call 
```python
print(encrypt23("flag"))
```
and the output will be <code>f6-116</code>

## Solution:
Great, so as long as we figure out the differences of ASCII values given the ciphertext, we can reverse the encryption logic and figure out the plaintext.

So far, we have that the difference between the second and first characters of the plaintext is 6.

Continue reading the ciphertext, we have the difference between the third and second characters of the plaintext is -1...right?

We can check this by printing out <code>ord("a")-ord("l")</code> which actually gives <code>-11</code>.

Ok. This is the main problem. There are numerous ways to interpret or 'break' the ciphertext into a list of numbers (the differences of ASCII values). I'm pretty sure through trial and error, one can eventually figure this out manually, but it's also possible to brute force all valid combinations.

### Breaking the ciphertext
Let's just consider this group of the ciphertext <code>11620</code> (we'll add the negative in later). There are 5 numbers, in which there are 4 slots for dividers. Each slot either has or does not have a divider, giving us a total of <code>2 to the 4th power</code> number of possible ways to block this.

To implement this, I used <code>itertools.product</code> to give all the combinations of <code>0</code> and <code>1</code> for length <code>len(group)-1</code>. Then, I go through each combination and if there's a <code>1</code>, then a space is inserted into that group of ciphertext, which will act as the divider.

```python
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
```
Of course, if that negative sign is detected, then the program will remember that, strip that negative character temporarily, and then add it in as the last step after all 'dividers' have been inserted.

### Putting it all together
The above code just takes care of one group of the ciphertext. It is up to the main program to create the groups, send them in, and then combine the 'divided' groupings together using yet again <code>itertools.product</code> into a grand list of numbers, representing the differences of ASCII values.
```python
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
```
## Comments...
See complete code at <code>solve.py</code>

I apologize for the one-liners and possibly overly complicated and inefficient logic. If you have any comments, improvements, and feedback, I'd love to hear them! 