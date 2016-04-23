## Upload image to https://imgur.com 

### What is this?

This script helps to upload your images to https://imgur.com and get back the
url for sharing.

### How to install

Firstly, you **MUST** [register](https://api.imgur.com/#registerapp) with
imgur.com to get your own unique key pairs. Having this pair doesn't mean you
have to login to upload image, this script upload images anonymously. 

- Export your keys

After received keys from imgur.com, export it as your environment variables:

```
$ export IMGUR_CLIENT_ID='your_client_id'
$ export IMGUR_CLIENT_SECRET='your_secret'
```


- (Optional but recommended) Create your own `virtualenv`
```
$ virtualenv pyimgur && cd pyimgur
```

- Clone this directory into your virtualenv

- Install dependency package
```
$ pip install -i requirements.txt
```

### How to use

Easy as pie!

```
$ python pyimgur.py [/path/to/image(s)]
```

- If upload only one file, will return url of that image.
```
$ python pyimgur.py ~/Pictures/brain.png 
http://i.imgur.com/MXSR5KW.png
```
- If upload multiple files, will return url of the album of those images.
```
$ python pyimgur.py ~/Pictures/{brain,loading,Jack4}.png 
https://imgur.com/a/oL1Um

```

### License

MIT
