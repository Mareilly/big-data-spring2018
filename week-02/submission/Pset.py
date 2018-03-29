
#PART A
snakes = ['viper','anaconda','mamba','cobra'] #A1 Create a list containing any 4 strings.
print snakes[2] #A2 Print the 3rd item in the list - remember how Python indexes lists!
print snakes [0:2] #A3 Print the 1st and 2nd item in the list using [:] index slicing.
snakes.append("last") #A4 Add a new string with text “last” to the end of the list and print the list.
print(snakes)
print len(snakes) #A5Get the list length and print it.

## Yes, but could also use negative indexing (i.e., snakes[-1] = 'new')
snakes[snakes.index('last')] = 'new' #A6 Replace the last item in the list with the string “new” and print
print snakes

#PART B
sentence_words = ['I', 'am', 'learning', 'Python', 'to', 'munge', 'large', 'datasets', 'and', 'visualize', 'them']

# Should be...
print (' '.join(sentence_words))

print (''.join(sentence_words)) #B1
print (''.join(reversed(sentence_words))) #B2
sentence_words.sort() #B3

sentence_words
print "".join(sorted(sentence_words)) #B4
# The sorted function returns a new sorted list and leaves the original list in tact, Sort is an in-place operation and returns "none".

#PART C
from random import randint
# this returns random integer: 100 <= number <= 1000
def my_random(y,x=0):
    num = randint(x,y)
    return (num)

#x=my_random(100,0)
#print x

assert(0 <= my_random(100) <= 100)
assert(50 <= my_random(100, x = 50) <= 100)

#PART D
def book_list (title, num):
    x = "The number {num} bestseller today is {title}".format
    print(x)
    return x
book_list("Sapiens", 1)

#PART E
password="" #enter password here

def password_checker(x):
    import string
    n=['0','1','2','3','4','5','6','7','8','9']
    u=string.ascii_lowercase.upper()
    s=['!', '?', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=']
    ok_l=[]
    ok_n=[]
    ok_u=[]
    ok_s=[]
    if 8<=len(x)<=14:
        ok_l.append(1)
    for i in x:
        if i in n:
            ok_n.append(i)
    for i in x:
        if i in u:
            ok_u.append(i)
    for i in x:
        if i in s:
            ok_s.append(i)
    if len(ok_l)==1 and len(ok_n)>=2 and len(ok_u)>=1 and len(ok_s)>=1:
        print ("NAILED IT")

    else:
        print ("Womp, womp, try again")

password_checker(password)

#PART F
def power(num,pow):
  number = 1
  for x in range(pow):
    number=number*num
  return number
power(2,3)
power(1, 0)
#this code created with help from human who goes by A-B-B (Stack OverFlow)
