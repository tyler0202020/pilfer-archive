#!/usr/bin/python
# -*- coding:utf-8 -*-
#--
#
# Name: pilfer-archive
# Description: Pilfer Archive.org for files to fuzz
# Author(s): level@coresecurity.com and jonathan.hardin@coresecurity.com
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. 
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, 
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT 
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR 
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGE.
#
#
#--
# configuration
log = True
debug = False
maxThreads = 100 # really maxThreads*3
# end

#code
import re, urllib2, socket, json, os, sys
from thread import start_new_thread
from time import sleep

itemz = ['flv', 'mov', 'mp4', 'ogm', 'ogg', 'mkv', 'mka', 'ts', 'mpg', 'mpg', 'mp3', 'mp2', 'nsc', 'nsv', 'nut', 'ram', 'rm', 'rv', 'rmbvtta', 'tac', 'ty', 'wav', 'dtsmpga', 'mp3', 'mp3', 'mp4a', 'HE-AACatrc', 'ilbcQCELP', 'lpcJ', '28_8', 'dnet', 'sipr', 'cook', 'atrc', 'raac', 'racp', 'ralf', 'vorb', 'dtswma1', 'wma2Apple', 'Monkeys Audio', 'Musepack', 'ADMPCM', 'rlesmcrpzaqdrw', 'sheervideo', 'corepng', 'msulossless', 'snow', 'pixlet', 'asv1asv2', 'tarkin', 'mpegmp1v', 'mpg1', 'pim1', 'mp2v', 'mpg2', 'vcr2', 'hdv1', 'hdv2', 'hdv3', 'mx*n', 'mx*p', 'div1', 'div2', 'div3', 'mp41', 'mp42', 'mpg4', 'mpg3', 'div4', 'div5', 'div6', 'col1', 'col0', '3ivd', 'divx', 'xvid', 'mp4s', 'm4s2', 'Xvid', 'mp4v', 'fmp4', '3iv2', 'smp4', 'h261', 'h262', 'h263', 'h264', 's264', 'avc1', 'davc', 'h264', 'x264', 'vssh', 'svq1', 'svq3', 'cvid', 'thra', 'wmv1', 'wmv2', 'wmv3', 'wvc1', 'wmva', 'vp31', 'vp30', 'vp3', 'vp50', 'vp5', 'vp51', 'vp6-', 'vp61', 'vp62', 'vp6f', 'vp6a', 'vp7', 'fsv1', 'iv31', 'iv32', 'iv41', 'iv51', 'rv10', 'rv13', 'rv20', 'rv30', 'rv40', 'bbcd', 'huffyuv', 'max', 'bpr', 'ace', 'img', 'rle', 'ima', 'im', 'aipd', 'arf', 'att', 'icn', 'sst', 'raw', 'awd', 'apx', 'g4', 'accacorn', 'adtphp', 'psd', 'ocp', 'art', 'pic', 'anv', 'frm', 'pix', 'als', 'alias', 'bmp', '2d', 'ami', 'iff', 'blk', 'info', 'cpc', 'avw', 'img', 'atk', 'hdru', 'hdr', 'gn', 'hdr', 'art', 'art', 'a64', 'ptg', 'awd', 'arn', 'pcp', 'sim', 'afx', 'img', 'fli', 'flc', 'cad', 'skf', 'skp', 'skb', 'gm', 'gm2', 'gm4', 'epa', 'ssp', 'b3d', 'bfl', 'bfli', 'fli', 'flp', 'afl', 'msk', 'img', 'raw', 'flt', 'blp', 'bmf', 'kap', 'sir', 'bmg', 'ibg', 'bfx', 'pic', 'pi', 'bob', 'pix', 'brk', '301', 'brt', 'uni', 'til', 'cal', 'cals', 'gp4', 'mil', 'cdu', 'cgm', 'dsi', 'cmu', 'cp8', 'csv', 'cpi', 'crg', 'raw', 'cr2', 'can', 'crw', 'big', 'cam', 'bay', 'raw', 'cmt', 'cip', 'clo', 'cloe', 'rix', 'sci', 'scx', 'sc?gif', 'giff', 'ce', 'ce1', 'ce2', 'bay', 'raw', 'idc', 'cdr', 'pat', 'bmf', 'cmx', 'cpt', 'ncd', 'nct', 'art', 'bay', 'rawmap', 'fpg', 'dis', 'dng', 'dpx', 'sd0', 'sd1', 'sd2', 'img', 'pi1', 'pc1', 'pi2', 'pc2', 'pi3', 'pc3', 'pi4', 'pi5', 'pi6', 'lbm', 'ilbm', 'dcm', 'acr', 'dic', 'dicom', 'dc3', 'tdim', 'img', 'gem', 'dds', 'cmpdol', 'doo', 'dd', 'jj', 'cut', 'drz', 'fsh', 'pix', 'ecc', 'tile', 'c4', 'trp', 'ei', 'eidi', 'bmc', 'ps', 'eps', 'eps', 'esmerf', 'eif', 'efx', 'ef3', 'iff', 'tdifit', 'fptg3', 'fax', 'fmf', 'fcxmap', 'fpg', 'mag', 'fi', 'ncyfts', 'fits', 'fit', 'bay', 'raw', 'bsg', 'f96', 'fx3', 'raf', 'fp2', 'fun', 'fpr', 'fbm', 'cbm', 'g16', 'gmf', 'geo', 'sul', 'gih', 'gig', 'xcf', 'gbr', 'ico', 'pat', '4bt', '4bit', 'clp', 'gun', 'ifl', 'wdp', 'hdp', 'hdr', 'hdri', 'hf', 'gro', 'grb', 'gro2', 'gro4', 'hp', 'hpg', 'hgl', 'plt', 'hpgl', 'hpgl2hru', 'raw', 'mdl', '3fr', 'jtf', 'hpi', 'hta', 'm8', 'hed', 'hir', 'hbm', 'lif', 'kps', 'pse', 'im5', 'imt', 'ica', 'ioca', 'mod', 'ipl', 'ithmb', 'iss', 'ifx', 'icl', 'fff', 'icb', 'mif', 'miff', 'ish', 'ish', 'ism', 'rlc', 'b&w', 'b_w', 'seq', 'g3n', 'img', 'img', 'iim', 'iph', 'ipt', 'itg', 'cit', 'rle', 'iimg', 'ct', 'irisjbg', 'bie', 'jbig', 'jb2', 'jpg', 'jpeg', 'jif', 'jfif', 'J', 'jpe', 'jpg', 'jpeg', 'jif', 'jfif', 'J', 'jpe', 'jxr', 'jls', 'jif', 'jig', 'vi', 'jng', 'btn', 'img', 'vif', 'viff', 'xv', 'thb', 'cel', 'koa', 'kla', 'gg', 'cin', 'kdc', 'k25', 'pcd', 'dcr', 'kfx', 'kro', 'kqp', 'lss', 'lvp', 'lda', 'mos', 'bay', 'raw', 'lwi', 'lff', 'celjpc', 'jp2', 'j2k', 'jpx', 'jpf', 'mag', 'pzp', 'mgr', 'mrc', 'mtv', 'mac', 'mpnt', 'macp', 'pntg', 'pnt', 'paint', 'icns', 'pic', 'pict', 'pict2', 'pct', 'rsc', 'rsrc', 'fff', 'pd', 't1', 't2', 'fre', 'mef', 'mrf', '411', 'mtx', 'pdx', 'bld', 'frm', 'pbt', 'mil', 'pp4', 'pp5', 'bay', 'raw', 'mic', 'msp', 'img', 'ipg', 'mrw', 'rfa', 'pdb', 'pdb', 'mphsc2', 'mng', 'ncr', 'pct', 'ntf', 'nitf', 'car', 'neo', 'npm', 'stw', 'nsr', 'ph', 'bn', 'img', 'nef', 'ngg', 'nlm', 'otb', 'nol', 'oaz', 'xfx', 'bmp', 'bga', 'ofx', 'orf', 'oil', 'exr', 'ctf', 'ttf', 'abs', 'hir', 'tap', 'bga', 'pix', 'pax', 'pic', 'clp', 'b16', 'pm', 'pcl', 'pmg', 'jbf', 'pspbrush', 'jbr','pfr', 'pspframe', 'psp', 'pspimage', 'pspmask', 'msk', 'pat', 'tub', 'psptube', 'tex', 'pdb', 'rw2', 'bay', 'raw', 'pxs', 'pxa', 'pef', 'art', 'pdd', 'pdb', 'pfi', 'fsy', 'frm', 'psf', 'stm', 'catp64', 'prc', 'mix', 'pic', 'pxr', 'picio', 'pixar', 'ib7', 'i17', 'i18', 'if9', 'pxa', 'pxb', 'pds', 'img', 'bms', '2bp', 'tsk', 'prf', 'pbm', 'rpbm', 'ppmapgm', 'rpgm', 'pnm', 'rpnm', 'pbm', 'rpbm', 'pgm', 'rpgm', 'ppm', 'rppm', 'png', 'apng', 'ppm', 'rppm', 'pgf', 'pgc', 'cvp', 'bum', 'ps', 'ps1', 'ps2crd', 'pps', 'ppt', 'pm', 'psa', 'psb', 'bs', 'pg', 'gb', 'cpa', 'pri', 'pic', 'mbm', 'ppp', 'pzl', 'q0', 'rgb', 'qdv', 'qrt', 'wal', 'vpb', 'qtif', 'qti', 'raw', 'icn', 'rad', 'img', 'pic', 'rp', 'raw', 'gry', 'grey', 'rawraw', 'gry', 'grey', 'rwz', 'pic', 'rsb', 'j6i', '001', 'ric', 'pig', 'xyz', 'rdc', 'ia', 'bay', 'raw', 'rpm', 'sar', 'st4', 'stx', 'st4', 'st5', 'st6', 'st7', 'st8', 'sci', 'sct', 'ct', 'ch', 'sfw', 'pwp', 'sfw', 'xp0', 'sj1', 'img', 'bmx', 'sif', 'x3f', 'rgb', 'rgba', 'bw', 'iris', 'sgi', 'int', 'inta', 'cs1', 'sti', 'skn', 'hrz', 'sdt', '001', 'pan', 'pic', 'si', 'sir', 'pmp', 'srf', 'tm2', 'tim', 'sr2', 'arw', 'spu', 'spc', 'sps', 'dat', 'ssi', 'pic', 'pac', 'seq', 'sdg', 'img', 'x', 'avs', 'mbfs', 'mbfavsjps', 'bay', 'rawicon', 'cursor', 'ico', 'pr', 'ras', 'rast', 'sun', 'sr', 'scr', 'rs', 'iff', 'vff', 'suniff', 'taac', 'syj', 'syn', 'synu', 'svg', 'tg4', '92i', '73i', '82i', '83i', '85i', '86i', '89i', 'tif', 'tim', 'tiff', 'imi', 'hr', 'pdb', 'mh', 'tnl', 'tjp', 'tny', 'tn1', 'tn2', 'tn3', 'b3d', 'b2d', 'gaf', 'tga', 'targa', 'pix', 'bpx', 'ivb', 'pst', 'upi', 'pe4', 'fac', 'face', 'rle', 'urt', 'v', 'vit', 'wrl', 'vfx', 'vif', 'vic', 'vicar', 'img', 'vid', 'vda', 'vst', 'img', 'pix', 'vob', 'wad', 'wsqrla', 'rlb', 'rpf', 'wb1', 'wbc', 'wbp', 'wbz', 'jig', 'webp', 'wepfxs', 'fxo', 'wfx', 'fxr', 'fxd', 'fxm', 'pic', 'ani', 'bmp', 'rle', 'vga', 'rl4', 'rl8', 'sys', 'clp', 'emz', 'wmz', 'cur', 'dib', 'ico', 'wzl', 'wbmp', 'wbm', 'wap', 'wpg', 'wfx', 'xwd', 'x11', 'xbm', 'bm', 'xpm', 'pm', 'p7', 'xar', 'xif', 'xim', 'smp', 'yuv', 'qtl', 'uyvy', 'yuv', 'qtl', 'uyvy', 'yuv', 'qtl', 'yuv', 'qtl', 'yuv', 'qtl', '$s', '$c', '!s', 'sna', 'scr', 'rgh', 'dta', 'lsm', 'zmf', 'zbr', 'dcx', 'pcx', 'pcc', 'dcx', 'bif', 'Legend', 'aif', 'aiff', 'au', 'snd', 'mdi', 'wav', 'mpg', 'm1v', 'mpa', 'ANI', 'CUR', 'AWD', 'B3D', 'CAM', 'CLP', 'CPT', 'CRWCR2', 'DCMACRIMA', 'DCX', 'DDS', 'DJVU', 'IW44', 'DXF', 'DXF', 'DWG', 'HPGL', 'CGM', 'SVG', 'ECW', 'EMF', 'EPS', 'PS', 'PDF', 'AI', 'EXR', 'FITS', 'FPX', 'FSH', 'G3', 'GIF', 'HDR', 'HDP', 'JXR', 'WDP', 'ICL', 'EXE', 'DLL', 'ICO', 'ICS', 'IFF', 'LBM', 'IMG', 'JP2', 'JPC', 'J2K', 'JPG', 'JPEG', 'JLS', 'JPM', 'KDC', 'MacPICT', 'QTIF', 'MNG', 'JNG', 'MRC', 'MrSID', 'SID', 'DNG', 'EEF', 'NEF', 'MRW', 'ORF', 'RAF', 'DCR', 'SRFARW', 'PEF', 'X3F', 'RW2', 'NRW', 'PBM', 'PCD', 'PCX', 'PDF', 'PDN', 'PGM', 'PNG', 'PPM', 'PSD', 'PSP', 'PVR', 'RAS', 'SUN', 'RAW', 'YUV', 'RLE', 'SFF', 'SFW', 'SGI', 'RGB', 'SIF', 'SWF', 'FLVTGA', 'TIF', 'TIFF', 'TTF', 'TXT', 'VTF', 'WAD', 'WAL', 'WBC', 'WBZ', 'WBMP', 'WebP', 'WMF', 'WSQ', 'XBM', 'XCF', 'XPM', 'AIF', 'AU', 'SND', 'MED', 'MID', 'MP3', 'OGG', 'RA', 'WAV', 'ASF', 'AVI', 'MOV', 'MP4', 'MPG', 'MPEG', 'WMA', 'WMV', 'PNG', 'JPG', 'BMP', 'GIF', 'TGA', 'DDS', 'TIFF', 'PDN', 'mbox', 'msf', 'MP3', 'MP4', 'Vorbis', 'FLAC', 'M3U', 'CUE', 'MP3', 'AIFF', 'WAV', 'MPEG-4', 'AAC', 'torrent', 'AVI', 'MPEG', 'mpg', 'mpe', 'm1v', 'm2v', 'mpv2', 'mp2v', 'pva', 'evo', 'm2p', 'MPEG-TS', 'ts', 'tp', 'trp', 'm2t', 'm2ts', 'mts', 'rec', 'VOB', 'IFO', 'MKV', 'webm', 'mp4', 'mov', '3gp', '3g2', 'flv', 'f4v', 'ogm', 'ogv', 'rm', 'ram', 'rt', 'tp', 'rmm', 'wmv', 'wmp', 'wm', 'asf', 'smk', 'bik', 'fli', 'flc', 'flic', 'dsm', 'dsv', 'dsa', 'dss', 'ivf', 'swf', 'divx', 'rmvb', 'amv', 'ac3', 'dts', 'aif', 'aifc', 'aiff', 'alac', 'amr', 'ape', 'apl', 'au', 'snd', 'cda', 'flac', 'm4a', 'm4b', 'm4r', 'aac', 'mid', 'midi', 'rmi', 'mka', 'mp3', 'mpa', 'mp2', 'm1a', 'm2a', 'mpc', 'ofg', 'ofs', 'ogg', 'oga', 'opus', 'ra', 'tak', 'tta', 'wav', 'wma', 'wv', 'aob', 'mlp', 'asx', 'm3u', 'm3u8', 'pls', 'wvx', 'wax', 'wmx', 'mpcpl', 'mpls', 'bdmv', 'PDF', 'XPS', 'DjVu', 'postscript', 'CHM', 'mobi', 'epub', 'fictionbook', 'flv', 'swf', '7z', 'ZIP', 'GZip', 'bzip2', 'xz', 'tar', 'WIM', 'APM', 'ARJ', 'CHM', 'cpio', 'DEB', 'FLV', 'JAR', 'LHALZH', 'LZMA', 'MSLZ', 'onepkg', 'RAR', 'RPM', 'smzip', 'SWF', 'xar', 'CramFS', 'DMG', 'FAT', 'HFS', 'ISO', 'MBR', 'NTFS', 'SquashFS', 'UDF', 'VHD', 'ARJ', 'LZH', 'TAR', 'GZ', 'ACE', 'UUE', 'BZ2', 'JAR', 'ISO', 'EXE', '7z', 'Z', 'RAR', 'xcf', 'xcfgzgzxcfgz', 'xcfbz2bz2xcfbz2', 'gbrgihpat', 'bmpdib', 'gif', 'htmhtml', 'ico', 'jpgjpegjpe', 'png', 'pnmppmpbm', 'pgmpam', 'pseps', 'psd', 'tga', 'tiftiff', 'xbm', 'xpm', 'pixmattemaskalphaals', 'fliflc', 'ch', 'dcmdicom', 'fitfits', 'cel', 'sgirgbbwicon', 'im1im8im24im32rasrs', 'pcxpcc', 'xwd', 'g3', 'wmfapm', 'psptub', 'pdf', 'svg', 'MJPEG', 'Motion', 'JPEG', '2000', 'MPEG-1', 'MPEG-2', 'Part', '2', 'MPEG-4', 'Part', '2ASP', 'Part', '10AVC', 'MPEG-H', 'Part', '2HEVC', 'H120', 'H261', 'H262', 'H263', 'H264', 'H265', 'Apple', 'Video', 'AVS', 'Bink', 'CineForm', 'Cinepak', 'Daala', 'Dirac', 'DV', 'FFV1', 'Huffyuv', 'Indeo', 'Microsoft', 'Video', '1', 'MSU', 'Lossless', 'Lagarith', 'OMS', 'Video', 'Pixlet', 'ProRes', '422', 'ProRes', '4444', 'QuickTime', 'Animation', 'Graphics', 'RealVideo', 'RTVideo', 'SheerVideo', 'Smacker', 'Sorenson', 'Video', 'Spark', 'Theora', 'Uncompressed', 'VC-1', 'VC-2', 'VC-3', 'VP3', 'VP6', 'VP7', 'VP8', 'VP9', 'WMV', 'XEB', 'YULS', 'MPEG-1', 'Layer', 'III', '(MP3)', 'MPEG-1', 'Layer', 'II', 'Multichannel', 'MPEG-1', 'Layer', 'I', 'AAC', 'HE-AAC', 'MPEG', 'Surround', 'MPEG-4', 'ALS', 'MPEG-4', 'SLS', 'MPEG-4', 'DST', 'MPEG-4', 'HVXC', 'MPEG-4', 'CELP', 'USAC', 'G711', 'G718', 'G719', 'G722', 'G7221', 'G7222', 'G723', 'G7231', 'G726', 'G728', 'G729', 'G7291', 'ACELP', 'AC-3', 'AMR', 'AMR-WB', 'AMR-WB+', 'ALAC', 'Asao', 'ATRAC', 'CELT', 'Codec2', 'DRA', 'DTS', 'EVRC', 'EVRC-B', 'FLAC', 'GSM-HR', 'GSM-FR', 'GSM-EFR', 'iLBC', 'iSAC', 'Monkeys', 'Audio', 'TTA', 'True', 'Audio', 'MT9', 'A-law', 'µ-law', 'Musepack', 'OptimFROG', 'Opus', 'OSQ', 'QCELP', 'RCELP', 'RealAudio', 'RTAudio', 'SD2', 'SHN', 'SILK', 'Siren', 'SMV', 'Speex', 'SVOPC', 'TwinVQ', 'VMR-WB', 'Vorbis', 'VSELP', 'WavPack', 'WMA', 'JPEG', 'JPEG', '2000', 'JPEG', 'XR', 'Lossless', 'JPEG', 'JBIG', 'JBIG2', 'PNG', 'TIFFEP', 'TIFFIT', 'HEVC', 'APNG', 'BMP', 'DjVu', 'EXR', 'GIF', 'ICER', 'ILBM', 'MNG', 'PCX', 'PGF', 'TGA', 'QTVR', 'TIFF', 'WBMP', 'WebP', 'MPEG-PS', 'MPEG-TS', 'ISO', 'base', 'media', 'file', 'format', 'MPEG-4', 'Part', '14', 'Motion', 'JPEG', '2000', 'MPEG-21', 'Part', '9', 'MPEG', 'media', 'transport', 'H2220', 'T802', '3GP', '3G2', 'AMV', 'ASF', 'AIFF', 'AVI', 'AU', 'Bink', 'DivX', 'Media', 'Format', 'DPX', 'EVO', 'Flash', 'Video', 'GXF', 'IFF', 'M2TS', 'Matroska', 'MXF', 'Ogg', 'QuickTime', 'File', 'Format', 'RatDVD', 'RealMedia', 'REDCODE', 'RIFF', 'Smacker', 'MOD', 'TOD', 'VOB', 'IFO', 'BUP', 'WAV', 'WebM']

def download(targetUrl):
	try:
		urlAddInfo = urllib2.urlopen(targetUrl)
		try:
			ext = targetUrl.split("/")[-1].split(".")[-1]
			if (ext not in itemz):
				return False
			else:
				fileName = targetUrl.split("/")[-1]
			data = urlAddInfo.read()
			if ("<html" not in data):
				try:
					if (os.path.exists("repo\%s" % (fileName)) != True):
						fp = open("repo\%s" % (fileName), "wb")
						fp.write(data)
						fp.close()
						if (log == True): print "[*] Wrote %s to file system" % (fileName)
						return True
					else:
						return False
				except Exception as e:
					if (debug == True): print "[*] error 5: %s" % (e)
					return False
			else:
				return False
		except Exception as e:
			if (debug == True): print "[*] error 4: %s" % (e)
			return False	
	except Exception as e:
		if (debug == True): print "[*] error 3: %s" % (e)
		return False
		
def archive_get_files(url):
	global itemz, maxThreads
	data = urllib2.urlopen(url).read()
	files = re.findall(r'href=[\'"]?([^\'" >]+)', data, re.UNICODE|re.MULTILINE)
	threads,thread_count = [], 0
	try:
		for i in xrange(0,len(files)):
			if (files[i].split(".")[-1] in itemz):
				if (thread_count < maxThreads):
					try:
						newThread = start_new_thread(download,("%s/%s" % (url,files[i]),))
						if (isinstance(newThread,int) != True):
							threads.append(newThread)
							thread_count+=1
						else:
							sleep(.5)
							i-=1
					except Exception as e:
						if (debug == True): print "[*] error 2: %s" % (e)
						sleep(.5)
						i-=1
				else:
					i-=1
					sleep(.5)
	except:
		#error spinning up new thread, move on with the threads we have available
		if (debug == True): print "[*] error <set me>: %s" % (e)
		pass
	for t in threads:
		t.join()
		thread_count-=1
	while True:
		try:
			if (thread_count > 0):
				sleep(1)
			else:
				#if we've reached zero we can break and return
				break	
		except Exception as e:
			#if an exception happens in archive_get_files() top level try/except the
			#thread_count variable never is set. Set the value and pass it back to the loop
			thread_count = 0
			pass
	return
		
def archive_get_location(item):
	try:
		data = json.loads(urllib2.urlopen("http://archive.org/details/%s&output=json&callback=IAE.favorite" % (item)).read()[13:-1])
	except:
		return
	url = "http://%s%s" % (data["server"],data["dir"])
	if (log == True): print "[*] directory location @ %s" % (url)
	archive_get_files(url)
	return

def archive_search(item):
	global maxThreads
	try:
		data = json.loads(urllib2.urlopen("http://archive.org/advancedsearch.php?q=%s&mediatype=&rows=1&page=1&output=json&save=no#raw" % (item)).read())
		print "[*] found %d entries for %s; grabbing all rows" % (data["response"]["numFound"],item)
		numFound = data["response"]["numFound"]
		data = json.loads(urllib2.urlopen("http://archive.org/advancedsearch.php?q=%s&mediatype=&rows=%d&page=1&output=json&save=no#raw" % (item,numFound)).read())
		if (numFound != 0):
			threads,thread_count = [],0
			for i in xrange(0,numFound):
				if (thread_count < maxThreads):
					try:
						if (" " in data["response"]["docs"][i]["title"]):
							newThread = start_new_thread(archive_get_location,(data["response"]["docs"][i]["title"].replace(" ","-"),))
							if (isinstance(newThread,int) != True):
								threads.append(newThread)
								thread_count+=1
							else:
								sleep(.5)
								i-=1
						else:
							newThread = start_new_thread(archive_get_location,(data["response"]["docs"][i]["title"],))
							if (isinstance(newThread,int) != True):
								threads.append(newThread)
								thread_count+=1
							else:
								sleep(.5)
								i-=1
					except Exception as e:
						if (debug == True): print "[*] error 1: %s" % (e)
						sleep(.5)
						i-=1
				else:
					sleep(.5)
					i-=1
		for t in threads:
			t.join()
			thread_count-=1
	except Exception as e:
		if (debug == True): print "[*] error 0: %s" % (e)
	while True:
		try:
			if (thread_count > 0):
				sleep(1)
			else:
				#if we've reached zero we can break and return
				break	
		except Exception as e:
			#if an exception happens in archive_search() top level try/except the
			#thread_count variable never is set. Set the value and pass it back to the loop
			thread_count = 0
			pass
	return
	
def disgard_exceptions(t,e,tb):
	# Disregard and restart main. Since 'itemz' is a global it won't affect progress
	if (debug == True): print "[*] Exception Received, restarting main()"
	main()
	return
		
def main():
	global itemz, maxThreads
	try:
		if (log == True): print "[*] looking for %d files types" % (len(itemz))
		threads,thread_count = [], 0
		for i in xrange(0,len(itemz)):
			if (thread_count < maxThreads):
				try:
					newThread = start_new_thread(archive_search,(itemz[i],))
					if (isinstance(newThread,int) != True):
						thread_count += 1
						if (log == True): print "[*] new thread spawned (%d/100)" % (thread_count),
						threads.append(newThread)
						itemz.remove(itemz[i])
					else:
						sleep(.5)
						i-=1
				except Exception as e:
					if (debug == True): print "[*] error -1: %s" % (e)
					sleep(.5)
					i-=1
			else:
				sleep(.5)
				i-=1
		for t in threads:
			t.join()
			thread_count -= 1			
	except KeyboardInterrupt:
		if (log == True): print "[*] User closed the session"
	except Exception as e:
		if (debug == True): print "[*] error -2: %s" % (e)
	while True:
		try:
			if (thread_count > 0):
				sleep(1)
			else:
				#if we've reached zero we can break and return
				break	
		except Exception as e:
			#if an exception happens in main() top level try/except the
			#thread_count variable never is set. Set the value and pass back to the loop.
			thread_count = 0
			pass
	if (log == True): print "[*] Done"
	sys.exit()
		
if __name__=="__main__":
	sys.excepthook = disgard_exceptions	
	main()
