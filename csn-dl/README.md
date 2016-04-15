

## Đây là gì?

Một script nhỏ giúp cho việc download các bài nhạc MP3 (320kbps) tại http://chiasenhac.com dễ dàng hơn. 


> **Tôi không chịu trách nhiệm về tính bản quyền của các bài hát tại trang
web trên**


## Sử dụng thế nào?

- Cài đặt các thư viện cần thiết:

```
$ pip install -r requirements.txt
```

- Tải file `csn-dl.py` về máy, gán quyền execute cho file này.


- Hiển thị các options:

```
$ ./csn-dl.py -h 

usage: csn-dl.py [-h] [-f FILENAME] [-s] [-d DIRECTORY] [-l LINK [LINK ...]]

All arguments

optional arguments:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        Specify input file contains album urls
  -s, --song            Make script to download songs instead album
  -d DIRECTORY, --directory DIRECTORY
                        Specify directory to store songs.
  -l LINK [LINK ...], --link LINK [LINK ...]
                        Specify url(s) to download

```

> Lưu ý: mặc định script này sẽ download album, nếu muốn download 1 bài hát, sử
> dụng option `-s`


- Download một bài hát:

```
$ ./csn-dl.py -s -l http://chiasenhac.com/mp3/us-uk/u-pop/nightmare~avenged-sevenfold~1019045.html
```

- Download nhiều bài hát từ file `songs.txt`:


```
$ cat songs.txt
http://chiasenhac.com/mp3/us-uk/u-pop/dear-god~avenged-sevenfold~1019049.html
http://chiasenhac.com/mp3/us-uk/u-pop/photograph~ed-sheeran~1441049.html

$ ./csn-dl.py -s -f songs.txt

```

- Download một album: 

```
$ ./csn-dl.py -l http://chiasenhac.com/nghe-album/photograph~ed-sheeran~1441049.html
```

- Download nhiều album từ file `albums.txt`:

```
$ ./csn-dl.py -f albums.txt
```

> Lưu ý: Mỗi dòng 1 url


- Các bài hát sẽ được download về thư mục `Downloaded/CSN-Songs` cùng thư mục với script.

- Các albums sẽ được download về thư mục `Downloaded/CSN-Albums/[album_name]`.


```

$ tree Downloaded
Downloaded/
├── CSN-Albums
│   └── Dear_God
│       ├── Afterlife - Avenged Sevenfold [MP3 320kbps].mp3
│       └── Dear God - Avenged Sevenfold [MP3 320kbps].mp3
└── CSN-Songs
    └── Nightmare - Avenged Sevenfold [MP3 320kbps].mp3

   
```

- Để lưu trữ vào thư mục khác, sử dụng option `-d path/to/dir`:

```
$ ./csn-dl.py -f albums.txt -d /home/cuong/Music/
```

## Giấy phép

[GPLv3](http://www.gnu.org/licenses/gpl-3.0.txt)

## Tác giả

Cuong Nguyen (cuongnguyen23 at gmail dot com)
