def CamelCase(string: str):
    string = string.title()
    string = string.translate({ord(c): None for c in
                               ["_", " ", ".", "-", ":", "@", "#", "!", "?", "(", ")", "[", "]", "{", "}", "/", "\\",
                                ",", "=", ">", "<", "|"]})
    return string
