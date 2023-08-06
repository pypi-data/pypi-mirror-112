""" My first flit package """
__version__ = "0.2"

def say(word):
    return word

if __name__ == '__main__':
    print(say("hello"))