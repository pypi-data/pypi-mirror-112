#####################################
## MibiPlot                        ##
## by mibi88                       ##
## Make plots in a console         ##
## Version : v.0.1                 ##
## License : GNU GPL v2            ##
#####################################

class Plot():
    def __init__(self, type, values, labels, height = None, width = None):
        self.type = type
        self.values = values
        self.labels = labels
        self.height = height
        self.width = width
        self.maxnblength = len(str(self.height))
    def bar(self):
        if self.height == None:
            self.height = 20
        i = 0
        lines = []
        ia = self.height
        ic = 0
        while ia != 0:
            line = ""
            ib = 0
            #print(self.maxnblength - len(str(ic)))
            line += str(ia)
            if len(str(ia)) < self.maxnblength:
                while ib != self.maxnblength - len(str(ia)):
                    line += " "
                    #print("+1")
                    ib += 1
            line += " -| "
            for value in self.values:
                if ia == self.height:
                    if int(value) > self.height:
                        line += "++ "
                    elif int(value) == self.height:
                        line += "TT "
                    else:
                        line += "   "
                else:
                    if value > self.height:
                        line += "|| "
                    elif int(value) == ia:
                        line += "TT "
                    elif ia < int(value):
                        line += "|| "
                    else:
                        line += "   "
            lines.append(line)
            ia -= 1
            ic += 1
        line = ""
        id = 0
        while id != self.maxnblength + 3:
            line += " "
            id += 1
        for value in self.values:
            line += "---"
        line += " "
        lines.append(line)
        labellenght = []
        for item in self.labels:
            labellenght.append(len(str(item)))
        biggestlabellenght = 0
        for item in labellenght:
            if item > biggestlabellenght:
                biggestlabellenght = item
        ie = 0
        while ie != biggestlabellenght:
            line = ""
            ig = 0
            while ig != self.maxnblength + 3:
                line += " "
                ig += 1
            line += " "
            for label in self.labels:
                if ie > len(str(label)) - 1:
                    char = " "
                else:
                    char = label[ie]
                line += char
                line += "  "
            lines.append(line)
            ie += 1
        return lines
    def buildstr(self, lines):
        str = ""
        for line in lines:
            str += line + "\n"
        return str
