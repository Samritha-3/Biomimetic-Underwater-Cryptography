import hashlib, os, time, csv #It contains the SHA-256 hashing engine, which converts raw inputs into fixed-length cryptographic signatures.

INPUT_CSV = 'outputs/tracking_data.csv'
#the hybrid key 
def generate_key(fish_coords):
    # Everything inside the function must be indented by 4 spaces
    nonce = os.urandom(16)
    timestamp = str(time.time_ns()).encode() #: This grabs the current system time down to a nanosecond (one-billionth of a second),it changes constantly
    
    if fish_coords:
        # Code inside the 'if' block needs 4 more spaces
        entropy = fish_coords.encode() + timestamp + nonce
        source = 'FISH'
    else:
        # Code inside the 'else' block needs 4 more spaces
        entropy = os.urandom(32) + timestamp + nonce
        source = 'FALLBACK' #FALLBACK Mode, it defaults to generating an extra 32 bytes of pure system randomness so the system never stops producing secure keys
        
    key = hashlib.sha256(entropy).hexdigest()# SHA-256—anyone can compute the hash if they have your inputs, but absolutely
    #no one can reverse the hash to figure out what your inputs were.
    return key, source

with open(INPUT_CSV, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        frame = row['frame']
        count = int(row['fish_count'])
        centers = row['centers']
        
        # Generates key using the filtered red-box coordinates
        key, src = generate_key(centers if count > 0 else '')#redirects to fallbackmode in case of no fishes on the screen ensuring security 
        print(f'Frame {frame:>4} | {src:<8} | {count} red fish | {key[:32]}...')
