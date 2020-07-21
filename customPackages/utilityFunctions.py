 
def truncateEmbedValue(value):
    extension = '...\n\nMessage exceeds embed limits'
    maxLen = 1024
    if len(value)>maxLen:
        return value[:(maxLen-len(extension))] + extension
    else:
        return value