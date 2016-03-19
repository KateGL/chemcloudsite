
def check_blocks(s, begin, end):
    meetings = 0
    for c in s:
        if c == begin:
            meetings += 1
        elif c == end:
            meetings -= 1
            if meetings < 0:
                return False
    return meetings == 0