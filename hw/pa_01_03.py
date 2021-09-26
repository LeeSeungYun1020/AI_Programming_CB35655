def puzzle():
    startingWord = "NAISNIENLGELTETWEORRSD"
    crossedOutLetters = list(startingWord[::2])
    remainingLetters = list(startingWord[1::2])

    print("Starting word:", startingWord)
    print("Crossed out letters:", " ".join(crossedOutLetters))
    print("Remaining letters:", " ".join(remainingLetters))


if __name__ == '__main__':
    puzzle()
