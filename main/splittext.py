
test = "das ist eine text zum testen einer funktion\n eins zwei drei vier \n funf sechs sieben acht"

def split_text (text) : 
    tooshort = ""
    new_text = text.strip().split('\n')
    finaltext = [] 

    for p in new_text:
        print(len(tooshort.split() )) 
        print(tooshort.split())

        tooshort += p

        print(tooshort)

        if len(tooshort.split() ) > 10:
            finaltext.append(tooshort)
            tooshort = ""
    finaltext.append(tooshort)
    print(finaltext)
        
        


split_text(test)
    


