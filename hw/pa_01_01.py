def word_replacement():
    sentence = input("Enter a sentence: ")
    origin = input("Enter word to replace: ")
    change = input("Enter replacement word: ")
    print(sentence.replace(origin, change))


if __name__ == '__main__':
    word_replacement()
