log = []
currentLine = 0
def ReportError(msg):
    log.append({"line": currentLine, "message": msg})