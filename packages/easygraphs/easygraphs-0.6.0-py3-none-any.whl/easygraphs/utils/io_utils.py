'''

Author: Zeng Siwei
Date: 2021-01-29 15:58:33
LastEditors: Zeng Siwei
LastEditTime: 2021-04-13 12:04:46
Description: 

'''
import numpy as np
import logging


def load_graph(filepath, header=None, sep="\t", dtype="int", subnodes=[]):
    logging.info("Loading graph file: " + filepath)
    src_nodes = []
    dst_nodes = []
    vals = []
    set_node = set(subnodes)
    with open(filepath) as f:
        if header is not None:
            next(f)
        for line in f:
            tokens = line.strip().split(sep)
            src = tokens[0]
            dst = tokens[1]
            try:
                src = int(src)
                dst = int(dst)
            except Exception as e:
                pass
            if len(set_node) == 0 or (src in set_node and dst in set_node):
                src_nodes.append(src)
                dst_nodes.append(dst)
            if len(tokens) == 2:
                pass
            elif len(tokens) == 3:
                vals.append(float(tokens[2]))
            else:
                raise Exception("FormatError: write your own readfile()")

    return src_nodes, dst_nodes, vals

def save_graph(src, dst, filepath, val = [], sep="\t", with_shape=False, with_weight=True, start_index=0):
    import logging
    if not val:
        val = [1] * len(src)
    n_x = int(np.max(src)+1)
    n_y = int(np.max(dst)+1)
    with open(filepath, "w") as wfp:
        if with_shape:
            wfp.write(sep.join([str(x+start_index) for x in (n_x, n_y)])+"\n")
        
        if with_weight:
            tmp = zip(src, dst, val)
        else:
            tmp = zip(src, dst)

        for item in tmp:
                wfp.write(sep.join([str(x+start_index) for x in item])+"\n")
    logging.info("File writed to: %s" % filepath)

def save_collection(collection, filepath, sep="\t"):
    with open(filepath, "w") as wfp:
        for item in collection:
            wfp.write("%s\n" % item)
    logging.info("File writed to: %s" % filepath)

def load_table(filename, sep="\t", header=None, dtype=None):
    list_col = []
    with open(filename, "r") as f:
        if header is not None:
            next(f)
        for i, line in enumerate(f):
            tokens = line.strip().split(sep)
            if i == 0:
                n_col = len(tokens)
                for j in range(n_col):
                    list_col.append([])
            for j, token in enumerate(tokens):
                if len(tokens) != n_col:
                    raise ValueError("Length error in line%s: %s" %(j, line))
                list_col[j].append(dtype(token) if dtype else token)
    return list_col



def save_matrix(matrix, filepath, sep="\t", save_as_edges=False, with_shape=False, start_index=0):
    assert isinstance(matrix, np.ndarray)
    shape = matrix.shape
    if len(shape) != 2:
        raise ValueError("Only support 2-d matrix.")
    with open(filepath, "w") as wfp:
        if with_shape:
            wfp.write(sep.join([str(x+start_index) for x in shape])+"\n")
        if save_as_edges == False:
            for i in range(shape[0]):
                wfp.write(sep.join([str(x+start_index) for x in matrix[i]])+"\n")
        else:
            for i in range(shape[0]):
                for j in range(shape[1]):
                    wfp.write(sep.join([str(x+start_index) for x in (i, j, matrix[i][j])])+"\n")
    logging.info("File writed to: %s" % filepath)
        

def save_dict(d, filepath, sep="\t"):
    with open(filepath, "w") as wfp:
        for key, value in d.items():
            wfp.write(str(key) + sep + str(value) + "\n")


def load_dict(filepath, sep="\t", dtype=None):
    _len = None

    d = dict()
    with open(filepath) as fp:
        for i, line in enumerate(fp):
            tokens = line.strip().split(sep)
            if i == 0:
                if dtype is not None and not isinstance(dtype, (list, tuple)):
                    _len = len(tokens)
                    dtype = [dtype] * _len
            
            if dtype is not None:
                tokens = [dtype[i](x) for i, x in enumerate(tokens)]

            key = tokens[0]
            value = tokens[1:]
            d[key] = value
    return d




class Downloader(object):
    '''
    Given an url, download it to filepath
	
    Usage: 
        if not os.path.exists(filepath):
            Downloader.download(url, filepath)
    '''

    @classmethod
    def download(cls, url, filepath):
        dirname = os.path.dirname(os.path.abspath(os.path.expanduser(filepath)))
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        fname = cls._download(url, dirname, overwrite=False)
        cls._extract_archive(fname, filepath)

    @classmethod
    def _download(cls, url, path=None, overwrite=True, sha1_hash=None, retries=5, verify_ssl=True, log=True):
        """Download a given URL.

        Codes borrowed from mxnet/gluon/utils.py

        Parameters
        ----------
        url : str
            URL to download.
        path : str, optional
            Destination path to store downloaded file. By default stores to the
            current directory with the same name as in url.
        overwrite : bool, optional
            Whether to overwrite the destination file if it already exists.
            By default always overwrites the downloaded file.
        sha1_hash : str, optional
            Expected sha1 hash in hexadecimal digits. Will ignore existing file when hash is specified
            but doesn't match.
        retries : integer, default 5
            The number of times to attempt downloading in case of failure or non 200 return codes.
        verify_ssl : bool, default True
            Verify SSL certificates.
        log : bool, default True
            Whether to print the progress for download

        Returns
        -------
        str
            The file path of the downloaded file.
        """
        import requests

        if path is None:
            fname = url.split('/')[-1]
            # Empty filenames are invalid
            assert fname, 'Can\'t construct file-name from this URL. ' \
                'Please set the `path` option manually.'
        else:
            path = os.path.expanduser(path)
            if os.path.isdir(path):
                fname = os.path.join(path, url.split('/')[-1])
            else:
                fname = path
        assert retries >= 0, "Number of retries should be at least 0"

        if not verify_ssl:
            warnings.warn(
                'Unverified HTTPS request is being made (verify_ssl=False). '
                'Adding certificate verification is strongly advised.')

        if overwrite or not os.path.exists(fname) or (sha1_hash and not check_sha1(fname, sha1_hash)):
            dirname = os.path.dirname(os.path.abspath(os.path.expanduser(fname)))
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            while retries+1 > 0:
                # Disable pyling too broad Exception
                # pylint: disable=W0703
                try:
                    if log:
                        print('Downloading %s from %s...' % (fname, url))
                    r = requests.get(url, stream=True, verify=verify_ssl)
                    if r.status_code != 200:
                        raise RuntimeError("Failed downloading url %s" % url)
                    with open(fname, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=1024):
                            if chunk:  # filter out keep-alive new chunks
                                f.write(chunk)
                    if sha1_hash and not check_sha1(fname, sha1_hash):
                        raise UserWarning('File {} is downloaded but the content hash does not match.'
                                        ' The repo may be outdated or download may be incomplete. '
                                        'If the "repo_url" is overridden, consider switching to '
                                        'the default repo.'.format(fname))
                    break
                except Exception as e:
                    retries -= 1
                    if retries <= 0:
                        raise e
                    else:
                        if log:
                            print("download failed, retrying, {} attempt{} left"
                                .format(retries, 's' if retries > 1 else ''))

        return fname

    @classmethod
    def check_sha1(cls, filename, sha1_hash):
        """Check whether the sha1 hash of the file content matches the expected hash.

        Codes borrowed from mxnet/gluon/utils.py

        Parameters
        ----------
        filename : str
            Path to the file.
        sha1_hash : str
            Expected sha1 hash in hexadecimal digits.

        Returns
        -------
        bool
            Whether the file content matches the expected hash.
        """
        sha1 = hashlib.sha1()
        with open(filename, 'rb') as f:
            while True:
                data = f.read(1048576)
                if not data:
                    break
                sha1.update(data)

        return sha1.hexdigest() == sha1_hash

    @classmethod
    def _extract_archive(cls, file, target_dir, overwrite=False, readmode="rb"):
        """Extract archive file.
        
        Codes borrowed from dgl/data/utils.py

        Parameters
        ----------
        file : str
            Absolute path of the archive file.
        target_dir : str
            Target directory of the archive to be uncompressed.
        overwrite : bool, default True
            Whether to overwrite the contents inside the directory.
            By default always overwrites.
        """
        if os.path.exists(target_dir) and not overwrite:
            return
        print('Extracting file to {}'.format(target_dir))
        if file.endswith('.tar.gz') or file.endswith('.tar') or file.endswith('.tgz'):
            import tarfile
            with tarfile.open(file, readmode) as archive:
                archive.extractall(path=target_dir)
        elif file.endswith('.gz'):
            import gzip
            import shutil
            with gzip.open(file, readmode) as f_in:
                with open(file[:-3], 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
        elif file.endswith('.zip'):
            import zipfile
            with zipfile.ZipFile(file, readmode) as archive:
                archive.extractall(path=target_dir)
        else:
            raise Exception('Unrecognized file type: ' + file)

