# `new_reader`

    read multicast, udp and http(s) like files.
  ---
  
  

![image](https://user-images.githubusercontent.com/52701496/205797792-aee34f1c-039c-427b-87f4-709c3b6a8aa2.png)

## Who uses new_reader.reader?

  * [threefive](https://github.com/futzu/threefive) 
  * [x9k3](https://github.com/futzu/x9k3)
  * [gumd](https://github.com/futzu/gumd) 
  * [m3ufu](https://github.com/futzu/m3ufu) 
  * [kabuki](https://github.com/futzu/kabuki) 
  * [iframes](https://github.com/futzu/iframes) 
 
 ## How is new_reader.reader used?
 ```
 # print a mpegts packet header via https
 
>>>> from new_reader import reader
>>>> with reader('https://so.slo.me/longb.ts') as rdr:
....     packet = rdr.read(188)
....     print(packet[:4])
....     
b'G@\x11\x10'

```

```lua
    stdin:              cat video.ts | gumd
    files:              "/home/you/video.ts"
    http(s) urls:       "https://example.com/vid.ts"
    udp urls:           "udp://1.2.3.4:5555"
    multicast urls:     "udp://@227.1.3.10:4310"
  ```
  ### UDP and Multicast
  * for UDP and Multicast, reader will set socket.SO_RCVBUF to twice the maximum value set in the OS. 
    * On OpenBSD 
    ```sh
    sysctl net.inet.udp.recvspace
    ```
    * On Linux
    ```lua
    sysctl net.core.rmem_max
    ```
    * On Windows
    ```lua
     I have no idea.
    ```

  
## Examples

- [x] Files
```lua
    from new_reader import reader

    with reader("/home/you/video.ts") as data:
        fu = data.read()
```
- [x] HTTP(S)
```lua
    from new_reader import reader

    with reader("https://futzu.com/xaa.ts") as data:
        fu = data.read()
```
- [x] Multicast
```smalltalk
    from new_reader import reader

    with reader("udp://@227.1.3.10:4310") as data:
        data.read(8192)
```
- [x] UDP
```lua
    from new_reader import reader

    udp_data =reader("udp://1.2.3.4:5555")
    chunks = [udp_data.read(188) for i in range(0,1024)]
    udp_data.close()
```
