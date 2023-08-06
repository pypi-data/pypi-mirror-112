def foustrindex(bgstr, ltstr):
    """
    This function is used to find all indexes of all the same substrings in a parent string.
    The first argument is used to fill in the parent string, the second argument is used to fill in the substring, this one
    The function finds the indexes of all the same strings in the parent string and returns them as a list. 
    """
    bigstr = []
    for st in range(len(bgstr) - len(ltstr)):
        if bgstr[st:st + len(ltstr)] == ltstr:
            bigstr.append(st)
    return bigstr;

def foustrtime(big, small):
    """
    This function is used to find the number of occurrences of all the same substrings in a parent string.
    The first argument is used to fill in the parent string, the second argument is used to fill in the substring, this one
    The function finds the number of occurrences of all the same strings in the parent string and returns them as int.
    """
    net = 0
    for number in range(len(big) - len(small)):
        if big[number:number + len(small)] == small:
            net += 1
    return net;


def replcbyind(sone,stwo,ione,itwo):
    """
    This function is used to replace strings. It is similar to Python's replace function
    Replace a string with another string, but replace the old string with the square of the string
    Formula, here it is in the way of index. The first parameter is used to fill in the parent string, the string to be replaced
    Include it, otherwise an error will be thrown. The second parameter is used to fill in the name to replace the old string with
    The new string, and the third argument is used to fill in the index of the old string.
    """
    get = list(sone)
    del get[ione:itwo +1]
    get.insert(ione,stwo)
    get0 = "".join(get)
    return get0;
