import time
import itertools

class Telex:

    __map = {
        "f" : {
            "a" : "à",
            "ă" : "ằ",
            "â" : "ầ",
            "e" : "è",
            "ê" : "ề",
            "i" : "ì",
            "o" : "ò",
            "ô" : "ồ",
            "ơ" : "ờ",
            "u" : "ù",
            "ư" : "ừ",
            "y" : "ỳ",
            "ươ": "ườ"
        },
        "s" : {
            "a" : "á",
            "ă" : "ắ",
            "â" : "ấ",
            "e" : "é",
            "ê" : "ế",
            "i" : "í",
            "o" : "ó",
            "ô" : "ố",
            "ơ" : "ớ",
            "u" : "ú",
            "ư" : "ứ",
            "y" : "ý",
            "ươ": "ướ" 
        },
        "x" : {
            "a" : "ã",
            "ă" : "ẵ",
            "â" : "ẫ",
            "e" : "ẽ",
            "ê" : "ễ",
            "i" : "ĩ",
            "o" : "õ",
            "ô" : "ỗ",
            "ơ" : "ỡ",
            "u" : "ũ",
            "ư" : "ữ",
            "y" : "ỹ",
            "ươ": "ưỡ"
        },
        "r" : {
            "a" : "ả",
            "ă" : "ẳ",
            "â" : "ẩ",
            "e" : "ẻ",
            "ê" : "ể",
            "i" : "ỉ",
            "o" : "ỏ",
            "ô" : "ổ",
            "ơ" : "ở",
            "u" : "ủ",
            "ư" : "ử",
            "y" : "ỷ",
            "ươ": "ưở"
        },
        "j" : {
            "a" : "ạ",
            "ă" : "ặ",
            "â" : "ậ",
            "e" : "ẹ",
            "ê" : "ệ",
            "i" : "ị",
            "o" : "ọ",
            "ô" : "ộ",
            "ơ" : "ợ",
            "u" : "ụ",
            "ư" : "ự",
            "y" : "ỵ",
            "ươ": "ượ"
        },
        "d" : {
            "d" : "đ"
        },
        "e" : {
            "e" : "ê"
        },
        "o" : {
            "o" : "ô"
        },
        "a" : {
            "a" : "â"
        },
        "w" : {
            "a" : "ă",
            "u" : "ư",
            "o" : "ơ",
            "uo" : "ươ"
        }
    }

    __mapChar = {
        "à" : "af",
        "á" : "as",
        "â" : "aa",
        "ã" : "ax",
        "è" : "ef",
        "é" : "es",
        "ê" : "ee",
        "ẹ" : "ej",
        "ẻ" : "ej",
        "ẽ" : "ex",
        "ì" : "if",
        "í" : "is",
        "ỉ" : "ir",
        "ị" : "ij",
        "ò" : "of",
        "ó" : "os",
        "ô" : "oo",
        "õ" : "ox",
        "ù" : "uf",
        "ú" : "us",
        "ý" : "ys",
        "ă" : "aw",
        "đ" : "dd",
        "ĩ" : "ix",
        "ũ" : "ux",
        "ơ" : "ow",
        "ư" : "uw",
        "ạ" : "aj",
        "ả" : "ar",
        "ấ" : "aas",
        "ầ" : "aaf",
        "ẩ" : "aar",
        "ẫ" : "aax",
        "ậ" : "aaj",
        "ắ" : "aws",
        "ằ" : "awf",
        "ẳ" : "awr",
        "ẵ" : "awx",
        "ặ" : "awj",
        "ế" : "ees",
        "ề" : "eef",
        "ể" : "eer",
        "ễ" : "eex",
        "ệ" : "eej",
        "ọ" : "oj",
        "ỏ" : "or",
        "ố" : "oos",
        "ồ" : "oof",
        "ổ" : "oor",
        "ỗ" : "oox",
        "ộ" : "ooj",
        "ớ" : "ows",
        "ờ" : "owf",
        "ở" : "owr",
        "ỡ" : "owx",
        "ợ" : "owj",
        "ụ" : "uj",
        "ủ" : "ur",
        "ứ" : "uws",
        "ừ" : "uwf",
        "ử" : "uwr",
        "ữ" : "uwx",
        "ự" : "uwj",
        "ỳ" : "yf",
        "ỵ" : "uj",
        "ỷ" : "yr",
        "ỹ" : "yx",
        "ươ" : "uow" ,
        "ưở": "uowr",
        "ướ": "uows",
        "ườ": "uowf",
        "ưỡ": "uowx",
        "ượ": "uowj",
    }

    def __init__(self, text):
        self.text = text

    def parseOne(self, word):
        for i, c in enumerate(word):
            if c in self.__map:
                replace = self.__map[c]
                for j in range(i - 1):
                    curChunk = ''.join(word[j:j+2])
                    if curChunk in replace:
                        nextWord = word[:j] + replace[curChunk] + word[j+2:i] + word[i+1:]
                        # print(nextWord)
                        return self.parseOne(nextWord)
                for j in range(i):
                    curChar = word[j]
                    if curChar in replace:
                        nextWord = word[:j] + replace[curChar] + word[j+1:i] + word[i+1:]
                        # print(curChar, nextWord)
                        return self.parseOne(nextWord)
        return word

    def parse(self):
        start = time.time()
        self.words = self.text.split()
        for i, word in enumerate(self.words):
            self.words[i] = self.parseOne(word)
        self.text = ' '.join(self.words)
        print("Done! %.2fs" % (time.time() - start))
        return self.text

    def invert(self):
        nsize, f = len(self.text), []
        for i in range(nsize + 1): f.append([])
        f[0] = ['']
        for i, c in enumerate(self.text):
            index, currentList = i + 1, []
            for j in range(index - 1, -1, -1):
                seqWord = self.text[j : index]
                if seqWord in self.__mapChar:
                    seqWord = self.__mapChar[seqWord]
                    beforeItems = f[j] if j >= 0 else ['']
                    for item in beforeItems:
                        currentList.append(item + seqWord)
            if len(currentList) == 0:
                for item in f[index - 1]:
                    currentList.append(item + c)
            # print(currentList)
            f[index] = currentList
        return f[-1]
