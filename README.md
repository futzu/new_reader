# reader
read multicast, udp and http(s) like files

  new_reader returns an open file handle.
```lua
    stdin:              cat video.ts | gumd
    files:              "/home/you/video.ts"
    http(s) urls:       "https://example.com/vid.ts"
    udp urls:           "udp://1.2.3.4:5555"
    multicast urls:     "udp://@227.1.3.10:4310"
  ```
  
  Use like:
```smalltalk
    from new_reader import reader

    with reader("udp://@227.1.3.10:4310") as data:
        data.read(8192)
        
    with reader("/home/you/video.ts") as data:
        fu = data.read()
        
    udp_data =reader("udp://1.2.3.4:5555")
    chunks = [udp_data.read(188) for i in range(0,1024)]
    udp_data.close()
```
