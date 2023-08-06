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
    return bigstr

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
    return net


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
    return get0
def replcdobstr(sone,stwo,sthree,ione):
    """
    This function is used to replace the NTH identical substring if there are multiple identical substrings in the same
    parent string. The first parameter is used to fill in the parent string. The second parameter is used to fill in the
    new string to be replaced with. The third parameter is used to fill in duplicate substrings. The fourth parameter is
    used to fill in the NTH repeated substring, with numbers. Since this is hard to understand, here's an example:
    STR = "123123123123123" # You can see that a string variable is created -- STR with 5 duplicates of 123. So I want
    to replace the fourth "123" with "456", so use this function and use it like the next line.
    str0 = replcdobstr(str,"456","123" ,3)
    print(str0)
    You should see that the result is "123123123456123". You should get the idea from the example.
    """
    get = list(sone)
    get0 = foustrindex(sone,sthree)
    del get[ione:ione + len(stwo)]
    get.insert(get0[ione],stwo)
    get1 = "".join(get)
    return get1
