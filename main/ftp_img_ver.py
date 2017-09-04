""" Verifies image file type """

import filetype, os

img_types = (
    'png', 'jpeg', 'jpg',
    'tiff', 'gif', 'bmp'
)

def verify_img_type(con):
    print 'VERIFYING image file types...'
    img_list = {}
    for root, dirs, files, in con.walk('.'):
        for x in files:
            if x.endswith(img_types):
                path = os.path.normpath(con.path.join(root, x))
                with con.open(path, 'rb') as f:
                    ba = bytearray(f.read())
                    kind = filetype.guess(ba)
                
                img_list[path] = {'mime': kind.mime, 'path': path}

    print '[DONE] Verify finished'
    return img_list