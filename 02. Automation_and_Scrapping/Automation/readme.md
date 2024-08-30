## How to select path
```
https://chromewebstore.google.com/detail/selectorshub-xpath-helper/ndgimibanhlabgdgjcpbbndiehljcpfh
```
## Find all element
```bash
//element_name        # example : //div , //p, //img
```
## Find all element and select by index (1--unlimited)
```bash
(//element_name)[1]   # example : (//div)[1] , (//p)[1]
```
## Find all element and select by index (1--unlimited)
```bash
(//element_name)[1]   # example : (//div)[1] , (//p)[1]
```
## Find by arribute
```bash
(//element_name[@arribute_name="value"])[1]       # example : (//div[@class="name"])[1] , (//div[@title="name"])[1] etc
```
## Loop logic
```py
elements = selector_all('//any-xpath')
for e in elements:
    print(e.text())
# Or
i = 1
while i < n:
    print(select(f'(//path)[{str(i)}]'))
    i+=1
```
## How to intertact JS click from browser devs
```
- from inspect element of targeted element
- right click > copy > copy js path
- insert copy in JS console (F12) and add .click() function and inter
```
