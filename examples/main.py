from nsupnp.simple import SimpleNsupnp
import os
import random

sc = SimpleNsupnp('DESK' + str(random.randint(1000, 9000)), 'NONE', 'NONE', '0.005')

while True:
    sr = sc.services()
    os.system('cls')
    print([i.name for i in sr])
    print([i.version for i in sr])
    print([i.protocol for i in sr])
    print([i.timeout for i in sr])
    print([i.address for i in sr])
