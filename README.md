bagustris@github
====================
A raw of [bagustris.github.io](https://bagustris.github.io).


## Building   

First, change permission to execute:  
```chmod -R 777 .
``` 

For docker version below 28:  
```
# for docker installed from source use docker compose
docker-compose -f docker-compose.yml up
```

For docker version 28 and above:  
```
docker compose -f docker-compose-28.yml up
```
For docker installed using snap, you may need to use `sudo`.