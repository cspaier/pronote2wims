import random
import string

def randomStringDigits(stringLength=6):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    #On exclue des caractères peu lisibles
    for i in 'lIO':
        lettersAndDigits=lettersAndDigits.replace(i,'')
        
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))
