import requests
import urllib
from os.path import dirname, abspath, join, exists
import os
import tarfile
import argparse
from zipfile import ZipFile

import utils

DATASETS = ['MR',
            'SST-1',
            'SST-2',
            'ag_news',
            'sogou_news',
            'dbpedia',
            'yelp_review_full',
            'yelp_review_polarity',
            'yahoo_answers',
            'amazon_review_full',
            'amazon_review_polarity']

BASE_DIR = dirname(abspath(__file__))
DATA_DIR = join(BASE_DIR, 'datasets')
if not exists(DATA_DIR):
    os.mkdir(DATA_DIR)

def download_dataset(dataset):
    
    if dataset in ['ag_news', 'amazon_review_full', 'amazon_review_polarity', 'dbpedia', 
                   'sogou_news', 'yahoo_answers', 'yelp_review_full', 'yelp_review_polarity']:
        download_from_google_drive(dataset)
    elif dataset == 'MR':
        download_mr()
    elif dataset == 'SST-1' or dataset == 'SST-2':
        download_sst()
    else:
        raise NotImplementedError()

def download_from_google_drive(dataset):
    
    google_drive_file_ids = {'ag_news':'0Bz8a_Dbh9QhbUDNpeUdjb0wxRms',
                      'amazon_review_full':'0Bz8a_Dbh9QhbZVhsUnRWRDhETzA',
                      'amazon_review_polarity':'0Bz8a_Dbh9QhbaW12WVVZS2drcnM',
                      'dbpedia':'0Bz8a_Dbh9QhbQ2Vic1kxMmZZQ1k',
                      'sogou_news':'0Bz8a_Dbh9QhbUkVqNEszd0pHaFE', 
                      'yahoo_answers':'0Bz8a_Dbh9Qhbd2JNdDBsQUdocVU',
                      'yelp_review_full':'0Bz8a_Dbh9QhbZlU4dXhHTFhZQU0',
                      'yelp_review_polarity':'0Bz8a_Dbh9QhbNUpYQ2N3SGlFaDg'
                     }
    file_id = google_drive_file_ids[dataset]
    download_file = '{dataset}.tar.gz'.format(dataset=dataset)
    destination = join(DATA_DIR, download_file)
    utils.download_file_from_google_drive(file_id, destination)
    with tarfile.open(destination, "r:gz") as tar:
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(tar, DATA_DIR)

def download_mr():
    dataset_dirname = 'MR'
    dataset_dir = join(DATA_DIR, dataset_dirname)
    if not exists(dataset_dir):
        os.mkdir(dataset_dir)
    dataset_url = 'https://www.cs.cornell.edu/people/pabo/movie%2Dreview%2Ddata/rt-polaritydata.tar.gz'
    tar_file = 'rt-polaritydata.tar.gz'
    tar_filepath = join(DATA_DIR, dataset_dir, tar_file)
    urllib.request.urlretrieve(dataset_url, filename=tar_filepath)
    with tarfile.open(tar_filepath, "r") as tar:
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(tar, dataset_dir)
        
def download_sst():
    # from https://nlp.stanford.edu/sentiment/
    dataset_url = 'https://nlp.stanford.edu/sentiment/trainDevTestTrees_PTB.zip'
    download_file = 'trainDevTestTrees_PTB.zip'
    download_filepath = join(DATA_DIR, download_file)
    dataset_dirname = 'SST'
    dataset_dir = join(DATA_DIR, dataset_dirname)
    urllib.request.urlretrieve(dataset_url, download_filepath)
    ZipFile(download_filepath).extractall(dataset_dir)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Download datasets")
    parser.add_argument("dataset", type=str, default='all', choices=DATASETS + ['all'])
    args = parser.parse_args()

    if args.dataset == 'all':
        for dataset in DATASETS:
            print("Downloading {dataset}...".format(dataset=dataset))
            download_dataset(dataset)
    else:
        download_dataset(args.dataset)