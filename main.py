import requests
import logging
import time
import os
from bs4 import BeautifulSoup
import youtube_dl
import argparse

def main():
    parser = argparse.ArgumentParser(description='Download videos from Patreon posts')
    parser.add_argument('url', type=str, help='The URL of the Patreon post')
    find_vimeo_videos(parser.parse_args().url)

def setup_logging():
    """
    Setup logging to console and file

    Parameters
    ----------
    None

    Returns
    -------
    logger : logging.Logger
        The logger object
    """
    epoch_time = int(time.time())
    if not os.path.exists('logs'):
        os.makedirs('logs')

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    handler = logging.FileHandler(filename=f'logs/{epoch_time}.log', mode='w')
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

def download_video(url):
    """
    Download a video from a given URL

    Parameters
    ----------
    url : str
        The URL of the video to download

    Returns
    -------
    None
    """
    ydl_opts = {}
    logger.info(f'Downloading video from {url}')
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
        except Exception as e:
            logger.error(f'Error downloading video from {url}: {e}')

def find_vimeo_videos(patreon_url):
    """
    Find Vimeo videos in a given Patreon post

    Parameters
    ----------
    patreon_url : str
        The URL of the Patreon post

    Returns
    -------
    None
    """
    logger.info(f'Getting {patreon_url}')
    try:
        r = requests.get(patreon_url)
    except Exception as e:
        logger.error(f'Error getting {patreon_url}: {e}')
        return

    logger.info(f'Parsing page')
    soup = BeautifulSoup(r.text, 'html.parser')
    num_iframes = len(soup.find_all('iframe'))
    
    logger.info(f'Found {num_iframes} iframes')
    i = 1
    for iframe in soup.find_all('iframe'):
        logger.info(f'Checking iframe {i} of {num_iframes}')

        src = iframe.get('src')
        if 'vimeo' in src:
            print(f'Found Vimeo video: {src}')
            download_video(src)

        i += 1

if __name__ == '__main__':
    logger = setup_logging()
    main()
