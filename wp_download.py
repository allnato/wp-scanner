""" Download WordPress files and hashes """
import requests, zipfile, os
from wp_diff import md5

dir_path = os.path.dirname(os.path.realpath(__file__)) + '\\wp-files'

def compare_zip_hash(ver):
    """ Returns true if the zip file is not tampered.

    Connects to the internet to verify WP hash.
    Also assumes the clean WP zip already exists.
    """
    
    print 'VERIFYING zip hash...'
    try:
        url = "https://wordpress.org/wordpress-{}.zip.md5".format(ver)
        r = requests.get(url, timeout=60)
        orig_zip_hash = r.text
    except requests.ConnectionError:
        print '[ERROR]: Conenction error'
        quit()
    except requests.Timeout:
        print '[ERROR]: Connection timeout'
        quit()
    
    fpath = '{}\\wordpress-{}.zip'.format(dir_path, ver)
    curr_zip_hash = md5(fpath)
    if curr_zip_hash != orig_zip_hash:
        print '[WARNING] Invalid hash'
        return False

    print '[DONE] Hash verified'
    return True

def extract(ver):
    """Extract a WordPress version in \\wp"""
    extract_path = dir_path + '\\{}'.format(ver)
    zip_filename = "wordpress-{}.zip".format(ver)
    zip_filepath = dir_path + '\\' + zip_filename

    # Check if zip exists
    if not os.path.exists(zip_filepath):
        print '[ERROR] wordpress-{}.zip not found'.format(ver)
        quit()

    # Create extract dir.
    if not os.path.exists(extract_path):
        print 'Creating {} directory'.format(extract_path)
        os.makedirs(extract_path)
    
    try:
        # Extract zip version
        print 'EXTRACTING ' + zip_filename
        z = zipfile.ZipFile(zip_filepath)
        z.extractall(extract_path)
    except (zipfile.BadZipfile, zipfile.LargeZipFile) as e:
        print '[ERROR] Bad/Large zip file'
    else:
        print '[DONE] Extract finish'
    

def download(ver):
    url = "https://wordpress.org/wordpress-{}.zip".format(ver)
    zip_filename = url.split('/')[-1]

    # Create wp-files if it doesn't exist
    if not os.path.exists(dir_path):
        print 'Creating /wp-files directory.'
        os.makedirs(dir_path)
    
    # Download version
    print 'DOWNLOADING {}...'.format(zip_filename)
    try:
        r = requests.get(url, stream=True, timeout=60)
        with open('{}\\{}'.format(dir_path, zip_filename), 'wb') as code:
            code.write(r.content)
    except requests.ConnectionError:
        print '[ERROR]: Conenction error'
        quit()
    except requests.Timeout:
        print '[ERROR]: Connection timeout'
        quit()

    print '[DONE] Download finished'

#download('4.7.5')





