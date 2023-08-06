def foustrindex(bgstr, ltstr):
    """
    这个函数用于找到一个母字符串中所有相同的子字符串的所有索引。
    第一个参数用于填写母字符串，第二个参数用于填写子字符串，这个
    函数找到母字符串中所有相同字符串的索引后，会将他们以列表的方式返回。
    """
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
    这个函数用于找到一个母字符串中所有相同的子字符串出现的次数。
    第一个参数用于填写母字符串，第二个参数用于填写子字符串，这个
    函数找到母字符串中所有相同字符串出现的次数后，会将他们以整数的方式返回。
    """

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
def replcapnt(sone,stwo,sthree):
    """
    这个函数是用来替换字符串的，他与python自带的replace功能相近，用于
    将某一个字符串替换为另一个字符串，只是replace的旧字符串以字符串的方
    式，这里则是以索引的方式。第一个参数用来填写母字符串，被替换的字符串
    要包括在其中，否则会抛出错误。第二个参数用于填写要将旧字符串替换为的
    新字符串，第三个参数用于填写旧字符串的索引。
    """
    """
    This function is used to replace strings. It is similar to Python's replace function
    Replace a string with another string, but replace the old string with the square of the string
    Formula, here it is in the way of index. The first parameter is used to fill in the parent string, the string to be replaced
    Include it, otherwise an error will be thrown. The second parameter is used to fill in the name to replace the old string with
    The new string, and the third argument is used to fill in the index of the old string.
    """
    get1 = list(sone)
    get1[sthree] = stwo
    get2 = "".join(get1)
    return get2;
