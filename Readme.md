link shortener cli.

## Usage 
```
Usage: slink [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  configure  Configure a service
  shorten    Shorten a link
```

## Usage examples

**Configure service**
```shell script
slink configure -S bitly
```
**Shorten a link**
 ```shell script
slink shorten https://russkie_vpered.com
```
or use a specific service
```shell script
slink shorten -S bitly https://russkie_vpered.com
```
