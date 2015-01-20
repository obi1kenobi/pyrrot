def pad_left(text, count, fillchar=' '):
    return (fillchar * count) + text

def count_left_padding(text):
    count = 0
    for c in text:
        if c == ' ':
            count += 1
        else:
            break
    return count
