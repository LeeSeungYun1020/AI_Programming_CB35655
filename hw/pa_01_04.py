def count_function(string, substring, start=None, end=None):
    string = string[start:end]
    cnt = 0
    pos = 0
    while True:
        pos = string.find(substring, pos)
        if pos == -1:
            break
        cnt += 1
        pos += len(substring)
    return cnt


if __name__ == '__main__':
    test_string = "kkkkaa"
    sub = "kk"
    print(test_string.count(sub))
    print(count_function(test_string, sub))