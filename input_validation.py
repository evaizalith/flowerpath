import re

# Scrubs input using a whitelist 
class inputManager():
    def __init__(self):
        self.stringVal = re.compile("[\\w\\s\\-'+]+")
        self.intVal = re.compile("\\d+")

    def text(self, input):
        ret = self.stringVal.match(input).group(0)
        return ret

    def int(self, input):
        ret = self.intVal.match(str(input)).group(0)
        return ret

def test():
    val = inputManager()

    goodString = "heehee I am the gooodest string in the world" 
    ret = val.text(goodString)
    print(f"Validating good string '{goodString}' -> '{ret}'")

    badString = "dhwhjdwh I am EVIL string\"\"''''+=+-_-@#)@8238923.,,;;;;eL:::338323 hogweed"
    ret = val.text(badString)
    print(f"Validating bad string '{badString}' -> '{ret}'")

    goodInt = 12345
    iret = val.int(goodInt)
    print(f"Validating good int {goodInt} -> {iret}")

    badInt = 1234.578
    iret = val.int(badInt)
    print(f"Validating bad int {badInt} -> {iret}")

if __name__ == "__main__":
    test()
