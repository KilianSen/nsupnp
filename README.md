# NSUPNP
nsupnp is the acronym for non standard universal plug and play. Its a small library that allows you to make devices or services discoverable on your network and find out about their use and usage.

## example

```python
from nsupnp.simple import SimpleNsupnp  
import os  
import random  
  
sc = SimpleNsupnp('Test' + str(random.randint(10000, 90000)), 'NONE', 'NONE', '0.005')  
  
while True:  
  sr = sc.services()  
  os.system('cls')  
  print([i.name for i in sr])  
  print([i.version for i in sr])  
  print([i.protocol for i in sr])  
  print([i.timeout for i in sr])  
  print([i.address for i in sr])
```


## example diagrams (often not rendered properly)


```mermaid
sequenceDiagram
exampleService -> Channel: r-regit * nSUPnP 1.0 <br/> inst: nSUPnP/alive <br/> maxt: 3 <br/> name: exampleService <br/> vers: 1.0.0 <br/> prot: tcp/ip <br/> addr: 192.168.178.11

AnotherExampleService -> Channel: r-regit * nSUPnP 1.0 <br/> inst: nSUPnP/alive <br/> maxt: 3  <br/> name: AnotherExampleService <br/> vers: 1.0.0 <br/> prot: tcp/ip <br/> addr: 192.168.178.34

Device0 -> Channel: s-search * nSUPnP 1.0 <br/> inst: nSUPnP/discover<br/> maxt: 3

exampleService -> Channel: r-regit * nSUPnP 1.0 <br/> inst: nSUPnP/byebye <br/> maxt: 3 <br/> name: exampleService <br/> vers: 1.0.0 <br/> prot: tcp/ip <br/> addr: 192.168.178.11

AnotherExampleService -> Channel: r-regit * nSUPnP 1.0 <br/> inst: nSUPnP/byebye <br/> maxt: 3  <br/> name: AnotherExampleService <br/> vers: 1.0.0 <br/> prot: tcp/ip <br/> addr: 192.168.178.34

exampleService -> Channel: r-regit * nSUPnP 1.0 <br/> inst: nSUPnP/alive <br/> maxt: 3 <br/> name: exampleService <br/> vers: 1.0.0 <br/> prot: tcp/ip <br/> addr: 192.168.178.11

AnotherExampleService -> Channel: r-regit * nSUPnP 1.0 <br/> inst: nSUPnP/alive <br/> maxt: 3  <br/> name: AnotherExampleService <br/> vers: 1.0.0 <br/> prot: tcp/ip <br/> addr: 192.168.178.34

```

