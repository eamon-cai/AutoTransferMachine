from loguru import logger
import time
import os
from utils.uploader.upload_tools import *
import re
import cloudscraper


def kimoji_upload(siteinfo, file1, record_path, qbinfo, basic, hashlist):
    url = siteinfo.url
    post_url = f"{url}takeupload.php"
    time_out = 40
    if (file1.pathinfo.type == 'anime' or file1.pathinfo.type == 'tv') and file1.pathinfo.collection == 0:
        fileinfo = file1.chinesename + '在' + siteinfo.sitename + '第' + file1.episodename + '集'
    else:
        fileinfo = file1.chinesename + '在' + siteinfo.sitename

    # 选择类型
    if 'anime' in file1.pathinfo.type.lower():
        select_type = '405'
        tags.append(14)
    elif 'show' in file1.pathinfo.type.lower():
        select_type = '403'
    elif 'tv' in file1.pathinfo.type.lower():
        select_type = '402'
    elif 'movie' in file1.pathinfo.type.lower():
        select_type = '401'
    elif 'doc' in file1.pathinfo.type.lower():
        select_type = '404'
    elif 'music' in file1.pathinfo.type.lower() or 'mv' in file1.pathinfo.type.lower() :
        select_type = '406'
    elif 'sport' in file1.pathinfo.type.lower():
        select_type = '407'
    else:
        select_type = '401'
    logger.info('已成功填写类型为' + file1.pathinfo.type)

    # 选择媒介
    if 'WEB' in file1.type.upper():
        medium_sel = '6'
        logger.info('已成功选择媒介为WEB-DL')
    elif 'UHD' in file1.type.upper():
        medium_sel = '10'
        logger.info('已成功选择媒介为UHD-BLURAY')
    elif 'BLU' in file1.type.upper():
        medium_sel = '1'
        logger.info('已成功选择媒介为BLURAY')
    elif 'ENCODE' in file1.type.upper():
        medium_sel = '7'
        logger.info('已成功选择媒介为ENCODE')
    elif 'HDTV' in file1.type.upper():
        medium_sel = '5'
        logger.info('已成功选择媒介为HDTV')
    elif 'REMUX' in file1.type.upper():
        medium_sel = '11'
        logger.info('已成功选择媒介为REMUX')
    elif 'DVD' in file1.type.upper():
        medium_sel = '3'
        logger.info('已成功选择媒介为DVD')
    elif 'CD' in file1.type.upper():
        medium_sel = '8'
        logger.info('已成功选择媒介为CD')
    elif 'MINI' in file1.type.upper():
        medium_sel = '4'
        logger.info('已成功选择媒介为CD')
    elif 'TRACK' in file1.type.upper():
        medium_sel = '9'
        logger.info('已成功选择媒介为CD')
    else:
        medium_sel = '12'
        logger.info('未识别到媒介信息，不选择媒介')

    # 选择编码
    if '264' in file1.Video_Format or 'AVC' in file1.Video_Format.upper():
        codec_sel = '1'
        logger.info('已成功选择编码为H264/AVC')
    elif '265' in file1.Video_Format.upper() or 'HEVC' in file1.Video_Format.upper():
        codec_sel = '6'
        logger.info('已成功选择编码为H265/HEVC')
    elif 'MPEG' in file1.Video_Format.upper():
        codec_sel = '4'
        logger.info('已成功选择编码为MPEG')
    elif 'MVC' in file1.Video_Format.upper():
        codec_sel = '10'
    elif 'XVID' in file1.Video_Format.upper():
        codec_sel = '3'
    elif 'VC' in file1.Video_Format.upper():
     codec_sel = '2'
    elif 'VP' in file1.Video_Format.upper():
     codec_sel = '7'
    elif 'AV' in file1.Video_Format.upper():
      codec_sel = '8'
    elif 'PRO' in file1.Video_Format.upper():
      codec_sel = '9'
    else:
        codec_sel = '5'
        logger.info('未识别到视频编码信息，不选择')

        # 选择音频编码
    if file1.Audio_Format.upper() == 'AAC':
        audiocodec_sel = '6'
    elif 'DTS' in file1.Audio_Format.upper() and 'X' in file1.Audio_Format.upper() and '7' in file1.Audio_Format.upper():
        audiocodec_sel = '9'
    elif 'DTS' in file1.Audio_Format.upper() and 'HD' in file1.Audio_Format.upper():
        audiocodec_sel = '8'
    elif 'DTS' in file1.Audio_Format.upper() and 'HR' in file1.Audio_Format.upper():
        audiocodec_sel = '15'
    elif 'TRUE' in file1.Audio_Format.upper() and 'ATMOS' in file1.Audio_Format.upper():
        audiocodec_sel = '10'
    elif 'TRUE' in file1.Audio_Format.upper():
        audiocodec_sel = '11'
    elif 'PCM' in file1.Audio_Format.upper():
        audiocodec_sel = '12'
    elif 'FLAC' in file1.Audio_Format.upper():
        audiocodec_sel = '1'
    elif 'APE' in file1.Audio_Format.upper():
        audiocodec_sel = '2'
    elif 'MP3' in file1.Audio_Format.upper():
        audiocodec_sel = '4'
    elif 'EAC3' in file1.Audio_Format.upper() or 'DDP' in file1.Audio_Format.upper():
        audiocodec_sel = '14'
    elif 'AC3' in file1.Audio_Format.upper() or 'DD' in file1.Audio_Format.upper():
        audiocodec_sel = '13'
    elif 'DTS' in file1.Audio_Format.upper():
        audiocodec_sel = '3'
    elif 'OGG' in file1.Audio_Format.upper():
        audiocodec_sel = '5'
    else:
        audiocodec_sel = '7'
    logger.info('已成功选择音频编码为' + file1.Audio_Format.upper())

    # 选择分辨率
    if '8K' in file1.standard_sel or '4320' in file1.standard_sel:
        standard_sel = '5'
    elif '2160' in file1.standard_sel or '4K' in file1.standard_sel :
        standard_sel = '6'
    elif '1080p' in file1.standard_sel.lower():
        standard_sel = '1'
    elif '1080i' in file1.standard_sel.lower():
        standard_sel = '2'
    elif '720' in file1.standard_sel:
        standard_sel = '3'
    else:
        standard_sel = '1'
    logger.info('已成功选择分辨率为' + file1.standard_sel)


    if '国' in file1.language or '中' in file1.language or '国语' in file1.pathinfo.tags:
        tags.append(5)
    if '粤' in file1.language or '粤语' in file1.pathinfo.tags:
        tags.append(12)
    if '简' in file1.sublan or '繁' in file1.sublan or '中' in file1.sublan or '中字' in file1.pathinfo.tags:
        tags.append(6)
    if '完结' in file1.pathinfo.tags:
        tags.append(13)
    if '杜比' in file1.pathinfo.tags or 'DOLBY' in file1.pathinfo.tags or 'Dolby' in file1.pathinfo.tags:
        tags.append(11)
    if 'DIY' in file1.pathinfo.tags:
        tags.append(4)
    if 'HDR' in file1.pathinfo.tags:
        tags.append(7)
    if 'MYTVS' in file1.pathinfo.uploadname.upper():
        tags.append(1)
    if 'NF' in file1.pathinfo.uploadname or 'NETFLIX' in file1.pathinfo.uploadname.upper():
        tags.append(8)
    tags = list(set(tags))
    tags.sort()

    if siteinfo.uplver == 1:
        uplver = 'yes'
    else:
        uplver = 'no'

    torrent_file = file1.torrentpath
    file_tup = ("file", (os.path.basename(torrent_file), open(torrent_file, 'rb'), 'application/x-bittorrent')),

    other_data = {
        "name": file1.uploadname,
        "small_descr": file1.small_descr + file1.pathinfo.exinfo,
        "url": file1.imdburl,
        "douban_id": file1.doubanurl,
        "color": "0",
        "font": "0",
        "size": "0",
        "descr": file1.pathinfo.contenthead + '\n' + file1.douban_info + '\n' + "[Mediainfo]" + file1.mediainfo + "[/Mediainfo]" + '\n' + file1.screenshoturl + '\n' + file1.pathinfo.contenttail,
        "type": select_type,
        "medium_sel": medium_sel,
        "codec_sel": codec_sel,
        "audiocodec_sel": audiocodec_sel,
        "standard_sel": standard_sel,
        "team_sel": team_sel,
        "uplver": uplver,
        "tags[]": tags,
    }

    scraper = cloudscraper.create_scraper()
    success_upload = 0
    try_upload = 0
    while success_upload == 0:
        try_upload += 1
        if try_upload > 5:
            return False, fileinfo + ' 发布种子发生请求错误,请确认站点是否正常运行'
        logger.info('正在发布种子')
        try:
            r = scraper.post(post_url, cookies=cookies_raw2jar(siteinfo.cookie), data=other_data, files=file_tup,
                             timeout=time_out)
            success_upload = 1
        except Exception as r:
            logger.warning('发布种子发生错误: %s' % (r))
            success_upload = 0

    return afterupload(r, fileinfo, record_path, siteinfo, file1, qbinfo, hashlist)