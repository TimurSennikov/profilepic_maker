from dotenv import load_dotenv

load_dotenv()

from pyro import *

i = int(input("Input offset to start with: "))

app.run(tinker_avatars(i))