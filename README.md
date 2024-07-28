# `new_reader` 
## Read `stdin`, `files`, `multicast`, `udp`, and `http(s)` URIs the same way.  
```python3
from new_reader import reader

rdr = reader('udp://@235.35.3.5:3535')
rdr.read()
```
  
## latest version is `0`.`1`.`11`  
* Critical Fix for Multicast

![image](https://user-images.githubusercontent.com/52701496/205797792-aee34f1c-039c-427b-87f4-709c3b6a8aa2.png)

## new_reader is used by [`threefive`](https://github.com/futzu/threefive), [`x9k3`](https://github.com/futzu/x9k3), [`gumd`](https://github.com/futzu/gumd), [`m3ufu`](https://github.com/futzu/m3ufu), [`superkabuki`](https://github.com/futzu/superkabuki), [`iframes`](https://github.com/futzu/iframes) , [`umzz`](https://github.com/futzu/umzz),[`showcues`](https://github.com/futzu/showcues),[`six2scte35`](https://github.com/futzu/six2scte35)and [`sideways`](https://github.com/futzu/sideways).

 
 ## How is `new_reader.reader` used?
 ```js
 # print a mpegts packet header via https
 
>>>> from new_reader import reader
>>>> with reader('https://so.slo.me/longb.ts') as rdr:
....     packet = rdr.read(188)
....     print(packet[:4])
....     
b'G@\x11\x10'
```
           
 
#### | more

- [x] `Files`
```js
    from new_reader import reader

    with reader("/home/you/video.ts") as data:
        fu = data.read()
```
- [x] `HTTP(S)`
```js
    from new_reader import reader

    with reader('http://iodisco.com/') as disco:
        disco.read()

    # Add http headers like this 
    
    with reader('http://iodisco.com/',headers={"myHeader":"DOOM"}) as doom:
        doom.read()

```
- [x] `Multicast`
```smalltalk
    from new_reader import reader

    with reader("udp://@227.1.3.10:4310") as data:
        data.read(8192)
```
- [x] `UDP`
```lua
    from new_reader import reader

    udp_data =reader("udp://1.2.3.4:5555")
    chunks = [udp_data.read(188) for i in range(0,1024)]
    udp_data.close()
```
  ### `UDP` and `Multicast`
  * reader will set `socket.SO_RCVBUF` to the maximum value allowed by the OS for `UDP` and `Multicast`.
  * `socket.SO_RCVBUF` can also be set like this:
    * On `OpenBSD` 
    ```js
    sysctl net.inet.udp.recvspace
    ```
    * On `Linux`
    ```js
      sysctl -w net.core.rmem_max=6815744
    ```
    * On `Windows`
    ```js
     I.have.no.idea
    ```
   
