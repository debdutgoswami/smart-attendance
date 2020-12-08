import random
import string

def randomString(n: int):
    """returns a random string which is in-turn used as the filename for the newly generated .wav file from ffmpeg
    
    Arguments:
        n {int} -- lenght of the random string
    
    Returns:
        str -- random string of size n
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(n))
