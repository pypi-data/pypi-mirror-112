# wl-wall/wl

wl is a simply python3 cli wallpaper manager for linux.

**NOTE**: wl use feh as wallpaper changer, install it on your system, on ubuntu:
`sudo apt-get install feh`

## Installing

```sh
python3 -m pip install wl-wall ## <- on linux
```

## Using

to get help use:

```sh
wl -h
```

Available commands are: config, set, ls, restore

### config command

The config command manage the configuration of wl.

The subcommands are: get, path
The optional arguments are: -h, -k|--key, -v|--value

#### Example of config command

To get the config use:

```sh
wl config get
```

To get the path use:

```sh
wl config path
```

To set the wallpapers_folder key in the config use:

```sh
mkdir ~/.wl.wallpapers
wl config -k wallpapers_folder -v ~/.wl.wallpapers
```

**NOTE**: The wallpapers folder is used to locate all wallpapers

### set command

The set command set a wallpaper by wallpaper name, it's
located in the `wallpapers_folder` config path, e.g:
if the `wallpapers_folder` are equal than `~/.wl.wallpapers`, the name `01.png`
are equal than `~.wl.wallpapers/01.png`

The positional arguments are: wallpaper
The optional arguments are: -h|--help

#### Example of set command

If you have a wallpaper named `01.jpg` and your `wallpapers_folder` are equal
than `~/.wl.wallpapers` you can use:

```sh
wl set 01.jpg
```

A complete example are:

```sh
mkdir -p ~/.wl.wallpapers
cd ~/.wl.wallpapers
curl -sL https://wallpapertag.com/wallpaper/full/a/1/8/799689-download-mac-os-wallpapers-1920x1200-for-ipad-2.jpg -o 01.jpg
cd
wl set 01.jpg
```

It changes your wallpaper

### ls command

The ls command show yours wallpapers located in `wallpapers_folder`

The optional arguments are: -h/--help, -it

#### Example of ls command

To show all available wallpapers use:

```sh
wl ls
```

To show all available wallpapers as bash iterable use:

```sh
wl ls -it
```

flag: -it is used for this:

```sh
for wallpaper in $(wl ls -it); do
    echo "A available wallpaper are $wallpaper"
done
```

### restore command

The restore command restore the before wallpaper, if you was set a wallpaper
`01.jpg` using `wl set 01.jpg`, in your config, set was created the `wallpaper`
key, with this value `$HOME/.wl.wallpapers/01.jpg`, the restore command use it.

The optional arguments are: -h/--help

### Example of restore command

An example of restore command are this:

```sh
wl restore
```

It restore your old wallpaper.

A complete example are with set and config:

```sh
mkdir ~/.wl.wallpapers && cd ~/.wl.wallpapers
curl -sL https://wallpapertag.com/wallpaper/full/a/1/8/799689-download-mac-os-wallpapers-1920x1200-for-ipad-2.jpg -o 01.jpg
wl config -k wallpapers_folder -v ~/.wl.wallpapers
wl set 01.jpg
feh --bg-scale ~/.wl.wallpapers/02.jpg ## or anyone wallpaper
wl restore ## this set 01.jpg
```

## Custom scripts

To create custom scripts you must use `bash` or `python`.

### Example scripts

- this script must be for into wallpapers array, it wallpapers array are wallpapers
names on the `~/.wl.wallpapers` folder, to it the python script are:

```python
from wl.commands.set import Set
from wl.scripts.arguments import arguments
from wl.core.wallpapers import wallpapers
from time import sleep


def set_wallpaper(wallpaper: str):
    wallpaper = arguments(wallpaper=wallpaper)
    Set(wallpaper)


def main():
    for wallpaper in wallpapers.get_wallpapers():
        set_wallpaper(wallpaper)
        sleep(1)


if __name__ == '__main__':
    main()
```

The bash script is:

```bash
for wallpaper in $(wl ls -it); do
    wl set "$wallpaper"
    sleep 1
done
```

- this script get the `PosixPaths` and names of wallpapers in the
`~/.wl.wallpapers` using the `fs` wl resource. Python script:

```python
from wl.resources.fs import fs
from pathlib import Path
from os.path import expanduser

fs.set_path(Path(expanduser('~')) / '.wl.wallpapers')
print(fs.get_path_content()) # this print a dict as this { [name]: [dirent] }
```

## Thanks for use me

Thanks for use wl-wall/wl.
