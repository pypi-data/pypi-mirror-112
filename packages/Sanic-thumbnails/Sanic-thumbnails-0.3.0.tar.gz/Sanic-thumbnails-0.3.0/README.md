Sanic-thumbnails
===============

A simple extension to create a thumbs for the Sanic


Installation
===============
Install with ``pip``:

Run ``pip install git+https://github.com/q8977452/sanic-thumbnails.git``

Add ``Thumbnail`` to your extension file:
    from sanic.ext.thumbnails import Thumbnail

    app = Sanic(__name__)

    thumb = Thumbnail(app)
    
Add ``MEDIA_FOLDER`` and ``MEDIA_URL`` in your settings:

    app.config['MEDIA_FOLDER'] = '/home/www/media'
    app.config['MEDIA_URL'] = '/media/'

Use in Jinja2 template:

    <img src="{{ 'image.jpg'|thumbnail('200x200') }}" alt="" />
    <img src="{{ 'image.jpg'|thumbnail('200x200', crop='fit', quality=100) }}" alt="" />


### Options

``crop='fit'`` returns a sized and cropped version of the image, cropped to the requested aspect ratio and size, [read more](http://pillow.readthedocs.org/en/latest/reference/ImageOps.html#PIL.ImageOps.fit).

``quality=XX`` changes the quality of the output JPEG thumbnail, default ``85``.


Develop and Production
===============

### Production

In production, you need to add media directory in you web server.


### Develop
To service the uploaded files need a helper function, where ``/media/`` your settings ``app.config['MEDIA_URL']``:

    @app.route("/upload", methods=['POST'])
    async def omo(request):
        from sanic import response
        import os
        import aiofiles
        if not os.path.exists(app.config['MEDIA_URL']):
            os.makedirs(app.config['MEDIA_URL'])
        async with aiofiles.open(app.config['MEDIA_URL']+"/"+request.files["file"][0].name, 'wb') as f:
            await f.write(request.files["file"][0].body)
        f.close()

        return response.json(True)


Option settings
===============

If you want to store the thumbnail in a folder other than the ``MEDIA_FOLDER``, you need to set it manually:

    app.config['MEDIA_THUMBNAIL_FOLDER'] = '/home/www/media/cache'
    app.config['MEDIA_THUMBNAIL_URL'] = '/media/cache/'