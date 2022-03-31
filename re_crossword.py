import sre_yield
import argparse
import string

# Παίρνω τα args από το terminal
parser = argparse.ArgumentParser()
parser.add_argument("csv_file")
parser.add_argument("txt_file")
args = parser.parse_args()

# Global μεταβλητές
found_words = {}
graph = {}
known_letters = {}
word_length = {}
regular_expressions = {}
used_regular_expressions = {}

# Φτιάχνω τον γράφο
def make_the_graph():
    global graph
    csv_file = args.csv_file
    with open(csv_file) as graph_input:
        for row in graph_input:
            nodes = [str(x) for x in row.split(",")]
            graph[nodes[0]] = [] 
            x = nodes[len(nodes) - 1]
            x = x[:1]
            nodes[len(nodes) - 1] = x
            for i in range(len(nodes)):
                if i != 0:
                    graph[nodes[0]].append(nodes[i])
    return graph

# Λεξικό που με True και False αναλόγως με το αν η λέξη έχει βρεθεί.
def found_the_words():
    global found_words
    global graph
    for row in graph:
        for col in graph[row]:
            if '.' not in col:
                found_words[row] = True
            else:
                found_words[row] = False
            break
    return found_words

# Βάζω τα γνωστά γράμματα σε λέξεις που δεν έχω βρει στον γράφο
def find_the_known_letters():
    global word_length
    global graph
    for row in graph:
        lista = graph[row]
        count = 0
        for char in lista[0]:
            if '.' == char:
                count += 1
        if count != word_length[row]:
            count = -1
            for col in lista:
                count += 1
                if count % 2 == 1:
                    pos = lista[count + 1]
                    lista_change = graph[lista[count]]
                    num = -1
                    for i in lista_change:
                        num += 1
                        if i == row and num % 2 == 1:
                            pos_change = lista_change[num + 1]
                    number = -1
                    a = lista[0]
                    for char in lista[0]:
                        number += 1
                        pos_change = int(pos_change)
                        if number == pos_change:
                            letter = a[pos_change]
                    a = lista_change[0]
                    number = -1
                    for char in lista_change[0]:
                        number += 1
                        pos = int(pos)
                        if number == pos and a[pos] == '.':
                            a = a[:pos] + letter + a[pos + 1:]
                    lista_change[0] = a
                    graph[lista[count]] = lista_change

# Βγάζω το γράμμα που έχει μπει στον γράφο από τη λάθος λέξη
def get_the_wrong_letters_out(w):
    lis = graph[w]
    count = -1
    for col in lis:
        count += 1
        if count % 2 == 1:
            cross_word = lis[count]
            cross_word_pos = lis[count + 1]
            if not found_words[cross_word]:
                lis1 = graph[cross_word]
                num = -1
                a = lis1[0]
                for char in a:
                    num += 1
                    cross_word_pos = int(cross_word_pos)
                    if num == cross_word_pos:
                        a = a[:cross_word_pos] + '.' + a[cross_word_pos + 1:]
                        break
                lis1[0] = a
                graph[cross_word] = lis1

# Λεξικό που περιέχει τον αριθμό των γνωστών γραμμάτων για κάθε λέξη
def numbers_of_known_letters():
    global known_letters
    global found_words
    global graph
    count_row_graph = -1
    for row in graph:
        known_letters[row] = 0
        count_row_graph += 1
        count = -1
        for col in graph[row]:
            count += 1
            if count == 0:
                for char in col:
                    if '.' != char:
                        known_letters[row] += 1
    return known_letters

# Λεξικό που περιέχει το μήκος κάθε λέξεις
def find_the_word_length():
    global word_length
    global graph
    for row in graph:
        for col in graph[row]:
            word_length[row] = len(col)
            break
    return word_length

# Λεξικό με τις κανονικές εκφράσεις
def find_regular_expressions():
    global word_length
    global regular_expressions
    max = -1
    for i in word_length:
        if word_length[i] > max:
            max = word_length[i]
    new_list = []
    txt_file = args.txt_file
    with open (txt_file) as regular_file_input:
        for row in regular_file_input:
            row = row.rstrip('\n')
            regular_expressions[row] = []
    for row in regular_expressions:
        regular_expressions[row] = list(sre_yield.AllStrings(row, max_count = 5, charset=string.ascii_uppercase))
        new_list.clear()
        for col in regular_expressions[row]:
            if len(col) <= max:
                new_list.append(col)
                regular_expressions[row] = new_list.copy()
    return regular_expressions

#Λεξικό με τις χρησιμοποιημένες κανονικές εκφράσεις
def find_used_reg_exp():
    global used_regular_expressions
    global graph
    for row in regular_expressions:
        used_regular_expressions[row] = False
        for col in regular_expressions[row]:
            for i in graph:
                lis = graph[i]
                if lis[0] == col:
                    used_regular_expressions[row] = True

# Βήμα 2
def find_an_unknown_word():
    global found_words
    global graph
    global known_letters
    global word_length
    max = -1
    for row in graph:
        if not found_words[row]:
            if known_letters[row] / word_length[row] > max:
                max = known_letters[row] / word_length[row]
                w = row
    return w

# Βήμα 3
def find_regular_expressions_of_word(word):
    global regular_expressions
    word_reg_exp = {} # Αυτές είναι οι κανονικές εκφράσεις που μπορούν να γεμίσουν τα τετράγωνα της συγκεκριμένης θέσης
    for row in regular_expressions:
        word_reg_exp[row] = []
        if not used_regular_expressions[row]:
            for col in regular_expressions[row]:
                if word_length[word] == len(col):
                    new_list_wo =[]
                    for char in graph[word][0]:
                        new_list_wo.append(char)
                    num = -1
                    flag = False
                    for i in col:
                        num += 1
                        if i != new_list_wo[num] and new_list_wo[num] != '.':
                            flag = True
                    if not flag:
                        word_reg_exp[row].append(col)
    return word_reg_exp

# Αλγόριθμος
def crossword():
    flag = False
    for i in found_words:
        if not found_words[i]:
            flag = True
            break
    if not flag:
        return True
    word = find_an_unknown_word()
    word_reg_exp = find_regular_expressions_of_word(word)
    if word_reg_exp != {}:
        for i in word_reg_exp:
            for j in word_reg_exp[i]:
                used_regular_expressions[i] = True
                found_words[word] = True
                graph[word][0] = j
                find_the_known_letters()
                numbers_of_known_letters()
                if crossword():
                    return True
                used_regular_expressions[i] = False
                found_words[word] = False
                lis = graph[word]
                a = lis[0]
                lis[0] = ''
                for j in range(len(a)):
                    lis[0] = lis[0] + '.'
                graph[word] = lis
                get_the_wrong_letters_out(word)
                find_the_known_letters()
                known_letters = numbers_of_known_letters()
    return False  

# Αρχή προγράμματος
if __name__ == '__main__':
    graph = make_the_graph()
    found_words = found_the_words()
    word_length = find_the_word_length()
    find_the_known_letters() # Βάζει τα γράμματα που ξέρω
    known_letters = numbers_of_known_letters()
    regular_expressions = find_regular_expressions()
    find_used_reg_exp()
    crossword()
    new_dict = {}
    for row in graph:
        new_dict[int(row)] = graph[row]
    new_dict = {k: v for k, v in sorted(new_dict.items())}
    for row in new_dict:
        a = 0
        lis = new_dict[row]
        for i in regular_expressions:
            for j in regular_expressions[i]:
                if j == lis[0]:
                    a = i
                    break
        print(row, end=' ')
        print(a, end=' ')
        print(lis[0])
