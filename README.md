# Cube puzzle

This repo implements two brute-force solvers for a wooden puzzle. The puzzle consists of a 64 block long snake that should be shaped into a 4x4x4 cube, see image below. ([image source](http://www.dr-karstens.de/snake.html))

![image](image.jpg)

The puzzle has (including rotations and mirroring) 192 solutions.

## Python implementation

Run with `python python/cube.py >python/solutions.txt 2>python/stats.txt`.
Does the job, but takes about [11.5 minutes](python/stats.txt) on my machine.

## C implementation

Compile with `gcc c/cube.c -Wall -Wextra -Ofast -o c/cube`.
Run with `./c/cube >c/solutions.txt 2>c/stats.txt`.
Takes about [1.6 seconds](c/stats.txt) on my machine.

## Results

Both implementations output exactly the same:
```
$ sha1sum c/solutions.txt python/solutions.txt
a351d700c7b702e74b128c875c60d0313f7b2aa5  c/solutions.txt
a351d700c7b702e74b128c875c60d0313f7b2aa5  python/solutions.txt
```

The C implementation is about 418 times as fast as the python implementation (on my machine):
```
$ tail -n 1 python/stats.txt c/stats.txt

==> python/stats.txt <==
  52,181,872 attempts |   682 sec | 76,532 attempts / sec | 192 solutions found | searching for (3,3,3)

==> c/stats.txt <==
    52181872 attempts |  1.6282 sec | 32048494 attempts / sec | 192 solutions found | searching for (3,3,3)
```

## My machine

```
$ neofetch
             ...-:::::-...                 luuk@argon
          .-MMMMMMMMMMMMMMM-.              ----------
      .-MMMM`..-:::::::-..`MMMM-.          OS: Linux Mint 20.3 x86_64
    .:MMMM.:MMMMMMMMMMMMMMM:.MMMM:.        Kernel: 5.4.0-107-generic
   -MMM-M---MMMMMMMMMMMMMMMMMMM.MMM-       Uptime: 4 hours, 59 mins
 `:MMM:MM`  :MMMM:....::-...-MMMM:MMM:`    Packages: 3311 (dpkg)
 :MMM:MMM`  :MM:`  ``    ``  `:MMM:MMM:    Shell: bash 5.0.17
.MMM.MMMM`  :MM.  -MM.  .MM-  `MMMM.MMM.   Resolution: 2560x1440, 1280x1024, 1280x1024
:MMM:MMMM`  :MM.  -MM-  .MM:  `MMMM-MMM:   DE: Xfce
:MMM:MMMM`  :MM.  -MM-  .MM:  `MMMM:MMM:   WM: Xfwm4
:MMM:MMMM`  :MM.  -MM-  .MM:  `MMMM-MMM:   WM Theme: Mint-Y-Dark
.MMM.MMMM`  :MM:--:MM:--:MM:  `MMMM.MMM.   Theme: Mint-Y-Dark [GTK2], Mint-Y [GTK3]
 :MMM:MMM-  `-MMMMMMMMMMMM-`  -MMM-MMM:    Icons: Mint-Y-Dark [GTK2], Mint-Y [GTK3]
  :MMM:MMM:`                `:MMM:MMM:     CPU: AMD Ryzen 9 3950X (32) @ 3.500GHz
   .MMM.MMMM:--------------:MMMM.MMM.      GPU: NVIDIA GeForce GTX 1060 6GB
     '-MMMM.-MMMMMMMMMMMMMMM-.MMMM-'       Memory: 4181MiB / 32081MiB
       '.-MMMM``--:::::--``MMMM-.'
            '-MMMMMMMMMMMMM-'
               ``-:::::-``

```
