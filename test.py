def isValid(s):
    """
    :type s: str
    :rtype: bool
    """
    my_dict = {
        '(': 0,
        ')': 0,
        '[': 0,
        ']': 0,
        '{': 0,
        '}': 0,
    }

    for i in range(int(len(s) / 2 - 1)):
        if s[i] == "(" and s[len(s) - i] == ")":
            continue
        if s[i] == "[" and s[len(s) - i] == "]":
            continue
        if s[i] == "{" and s[len(s) - i] == "}":
            continue
        return False


    for i in range(len(s)):
        my_dict[s[i]] += 1

    return (my_dict['('] == my_dict[')']) and (my_dict['['] == my_dict[']']) and (my_dict['{'] == my_dict['}'])

s = input('a:')
print(isValid(s))
