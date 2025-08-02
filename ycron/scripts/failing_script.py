import sys
import random

if random.random() > 0.5:
    print("This script failed!")
    sys.exit(1)
else:
    print("This script succeeded!")
    sys.exit(0)
