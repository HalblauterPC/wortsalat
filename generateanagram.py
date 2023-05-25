
hasanelement = False

english = True
wordlist=[]


# Read in the word list for a specific language (txt file separates words with each new line, recommended to reduce the number of small words (len <= 3))
if english:
    with open('popular.txt','r') as f:
        for line in f:
            strip_lines=line.strip()
            word = strip_lines.split()
            if hasanelement:
                if word[0].lower() != wordlist[-1]: 
                    wordlist.append(word[0].lower())
            else: 
                wordlist.append(word[0].lower())
                hasanelement = True

    wordlist = sorted(wordlist, key=len, reverse = True)
else:
    with open('wortliste.txt','r', encoding='utf-8') as f:
        for line in f:
            strip_lines=line.strip()
            word = strip_lines.split()
            if hasanelement:
                if word[0].lower() != wordlist[-1]: 
                    wordlist.append(word[0].lower())
            else: 
                wordlist.append(word[0].lower())
                hasanelement = True

    #wordlist = sorted(wordlist, key=len, reverse = True)

word = "johndoe" # all lower case

length = len(word)

#the letters are saved as dictionary of occurences
composition = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0, 
                'm': 0, 'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0,
                'y': 0, 'z': 0, 'ä': 0, 'ö': 0, 'ü': 0, 'ß': 0}

# get composition
for letter in word:
    composition[letter] += 1


# how many letters are in a composition
def evaluate(composition):
    sum = 0
    for letter in word:
        sum += composition[letter]
    return sum

# remove all words that are not possible with a letter composition
def sortout(i_wordlist, composition):
    wordlist = i_wordlist.copy()
    deleted = []
    #delete words
    #by length/ missing letters
    for index, testword in enumerate(wordlist):
        if len(testword) <= length:
            m_composition = composition.copy()
            i = 0
            while i < len(testword):
                letter = testword[i]
                m_composition[letter] -= 1
                if m_composition[letter] < 0:
                    deleted += [index]
                    i = len(testword)
                i += 1
        else:
            deleted += [index]
    offset = 0
    for i in deleted:
        wordlist.pop(i-offset)
        offset += 1
    return wordlist

wordlist = sortout(wordlist, composition)

# recursively reduce the letter composition with possible words to arraive at a finished anagram
def narrowdown(wordlist, composition, cache = "", hit = 0, maxlet = 0, lastword = "", depth = 0):
    if lastword == "": 
        for letter, number in composition.items():
            if (number > 0): lastword += letter*number
    match = 0
    n = evaluate(composition)

    max_match = 50000 # do not bother finding more than 50k anagrams

    if n == 0: return 1, [str(cache)]
    if n < maxlet:
        if n == 1 and hit < 1: return 0, []
        else:
            string = ""
            for letter, number in composition.items():
                if (number > 0): string += letter*number
            if cache == "": return 1, [str("~~  " + string)]
            else: return 1, [str("~~  "+ cache + "+" + string)]
    if wordlist == []: 
        if n == 1:
            if hit >= 1:
                string = ""
                for letter, number in composition.items():
                    if (number > 0): string += letter*number
                if cache == "": return 0, [str("-    " + string)]
                else: return 0, [str("-    "+ cache + "+" + string)]
            else: return 0, []
        if n == 2:
            if hit >= 2:
                string = ""
                for letter, number in composition.items():
                    if (number > 0): string += letter*number
                if cache == "": return 0, [str("--      " + string)]
                else: return 0, [str("--      "+ cache + "+" + string)]
            else: return 0, []
        else: return 0, []
    else:
        output = []
        newmatch = 0
        x = 0
        for testword in wordlist:
            if not ((depth == 0 and len(testword) < 4) or match >= max_match):
                if len(testword) <= len(lastword):
                    new_composition = composition.copy()
                    for letter in testword:
                        new_composition[letter] -= 1
                    nextstep = sortout(wordlist, new_composition)
                    if cache == "": newmatch, newoutput =  narrowdown(nextstep, new_composition, str(testword), lastword=testword, depth=depth+1)
                    else: newmatch, newoutput =  narrowdown(nextstep, new_composition, str(cache+"+"+testword), lastword=testword, depth=depth+1)
                    output += newoutput
                    match += newmatch
        if (x): print(x)
        return match+newmatch, output


matches, anagrams = narrowdown(wordlist, composition)

print(matches, " matches found.")

if english:
    with open('{}-anagrams-eng.txt'.format(word), 'w') as f:
        for item in anagrams:
            f.write("%s\n" % item)
else:
    with open('{}-anagramme.txt'.format(word), 'w') as f:
        for item in anagrams:
            f.write("%s\n" % item)

