import os
import json
import logging

# import coloredlogs
# coloredlogs.install(level='WARNING')


def get_logger(
        level=logging.INFO,
        format='[%(asctime)s \033[1m%(funcName)s\033[0m %(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        verbose=False, **kwargs):

    if verbose:
        level = logging.DEBUG

    logging.basicConfig(level=level, format=format, datefmt=datefmt)

    return logging.getLogger(__name__)


def safe_open(filename, mode='rb'):
    
    if 'w' in mode:
        dirname = os.path.dirname(filename)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)

    if filename.endswith('.gz'):
        import gzip
        return gzip.open(filename, mode=mode)

    return open(filename, mode=mode)


def extract_qcstat(filename):

    if filename.endswith('.zip'):
        import zipfile
        f = zipfile.ZipFile(filename)
        qcstat = [each.filename for each in f.filelist if 'qcstat.xls' in each.filename]
        try:
            return f.open(qcstat[0])
        except IndexError:
            return None
    else:
        import tarfile
        f = tarfile.open(filename)
        qcstat = [each for each in f.getnames() if 'qcstat.xls' in each]
        try:
            return f.extractfile(qcstat[0])
        except IndexError:
            return None


def get_qcstat(qcstat=None, report=None):
    if qcstat:
        return safe_open(qcstat)
    elif report:
        return extract_qcstat(report)


