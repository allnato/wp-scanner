""" Diff wordpress files via their MD5 hash """
import os, hashlib

def md5(fname, r_mode='rb'):
    """ Returns a md5 hash string of a given filename """

    hash_md5 = hashlib.md5()
    with open(fname, r_mode) as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def get_hash_dict(fpath):
    """ Returns a hash dictionary of php files inside the given directory """

    root_count = fpath.count(os.path.sep)
    hash_dict = {}
    for root, dirs, files in os.walk(fpath):
        for x in files:
            if x.endswith('.php'):
                path = os.path.join(root, x)
                path_count = path.count(os.path.sep)
                key_path = path.split('\\')[-(path_count - root_count):]
                hash_dict[os.path.join(*key_path)] = {'hash': md5(path), 'path': path}
    
    return hash_dict

def file_hash_diff(clean_wp_path, current_wp_path):
    """ Returns a hash diff dictionary of two wp directories. 
    
    The dictionary contains an array of diff files which include their metadata.
    These metadata include:
    kind = 'E' if the file is edited and 'N' if it's a new file,
    location = Location of the filename,
    wp_location = Location of the clean wp_file
    """

    print 'GENERATING hash dictionary'
    orig_hash = get_hash_dict(clean_wp_path)
    curr_hash = get_hash_dict(current_wp_path)
    print '[DONE]: Hash dictionary created'

    print 'COMPARING file hashes...'
    diff_hash = {
        'diff_e_count': 0, # Total number of edited files.
        'diff_n_count': 0, # Total number of new (unique) files.
        'diff_d_count': 0 # Total number of deleted files.
    }
    diff = [] # Holds all diff data
    # Find Edited and New files
    for key in curr_hash:
        if key in orig_hash:
            if curr_hash[key]['hash'] != orig_hash[key]['hash']:
                diff_hash['diff_e_count'] += 1
                diff.append({
                    'type': 'E',
                    'filename': key, 
                    'location': curr_hash[key]['path'],
                    'file_hash': curr_hash[key]['hash'],
                    'wp_hash': orig_hash[key]['hash'],
                    'wp_location': orig_hash[key]['path']
                })
        else:
            diff_hash['diff_n_count'] += 1
            diff.append({
                'type': 'N',
                'filename': key,
                'location': curr_hash[key]['path'],
                'file_hash': curr_hash[key]['hash']
            })
    
    # Find deleted files
    for key in orig_hash:
        if key not in curr_hash:
            diff_hash['diff_d_count'] += 1
            diff.append({
                'type': 'D',
                'filename': key,
                'wp_location': orig_hash[key]['path']
            })
    
    diff_hash['diff'] = diff
    print '[DONE]: File hash compared'
    return diff_hash
