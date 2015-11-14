# encoding: UTF-8
from __future__ import division
import os
import re
import sys
import shutil
import codecs


__author__ = 'Administrator'


def check_assline_format(ass_units):
    if len(ass_units) <= 8:
        return False
    i = 0
    for one_unit in ass_units:
        if i == 0 and not re.match("^D.*?", one_unit):
            return False
        if i == 3 and not re.match("Default", one_unit):
            return False
        i += 1

    return True


def check_file_or_dir(in_param):
    if os.path.isfile(in_param) and not os.path.exists(in_param):
        message = 'file, the "%s" can not be found. \n'
        sys.stdout.write(message)
        return False
    if os.path.isdir(in_param) and not os.path.exists(in_param):
        message = 'dir, the "%s" can not be found. \n'
        sys.stdout.write(message)
        return False
    return True


def get_filename_from_longdir(long_dir):
    if os.path.exists(long_dir):
        file_name = os.path.split(long_dir)[-1]
        return file_name
    else:
        return ""



def split_ass_line(ass_line):
    ass_line.strip(" \n")
    if len(ass_line) <= 50:
        return
    split_results = ass_line.split(",", 9)
    basic_info = []
    if len(split_results) >= 9 and check_assline_format(ass_units=split_results):
        i = 0
        for a_unit in split_results:
            sys.stdout.write("This unit is : " + a_unit + "\n")
            if i == 1:
                start_time = convert_asstime2secs(time_str=split_results[i])
                basic_info.append(str(start_time))
            if i == 2:
                end_time = convert_asstime2secs(time_str=split_results[i])
                basic_info.append(str(end_time))
            i += 1
        last_unit = split_results[-1]
        last_unit.replace("!",  " ")
        last_unit.replace("?",  " ")
        last_unit.replace("\\",  " ")

        basic_info.append(last_unit)
    return basic_info





def TimeStr2Secs(timeStr):
    timeArray = timeStr.split(",")
    hourMinSec = timeArray[0].split(":")
    secTime = float(hourMinSec[0])*3600 + float(hourMinSec[1])*60 + float(hourMinSec[2]) + float(timeArray[1])/1000
    return str(secTime)

def convert_asstime2secs(time_str):
    time_array = time_str.split(".")
    hour_min_sec = time_array[0].split(":")
    absolute_sec = float(hour_min_sec[0])*3600 + float(hour_min_sec[1])*60 + float(hour_min_sec[2]) + float(time_array[1])/1000
    return absolute_sec


def make_standard_index_format(text_header, curr_index):
    std_index = "%08d" % curr_index
    return text_header + str(std_index)


def merge_short_interval(in_list, min_interval_in_sec = 5):
    if len(in_list) < 2:
        return in_list
    list_index = 0
    compacted_result_list = []
    while list_index < len(in_list):
        attempt_index = 1
        while (float(in_list[list_index]["end"]) - float(in_list[list_index]["start"]) <  min_interval_in_sec):
            if (list_index + attempt_index) < (len(in_list)):
                attempt_unit = in_list[list_index + attempt_index]
                in_list[list_index]["end"] = attempt_unit["end"]
                in_list[list_index]["text"] += attempt_unit["text"]
                attempt_index += 1
            else:
                break
        compacted_result_list.append(in_list[list_index])
        list_index += attempt_index

    return compacted_result_list


def ChompDoubleSideSymbol(oneChar):
    localChar = oneChar
    allCharList = list(localChar)
    if len(allCharList) == 0:
        return localChar
    symbolRe = re.compile(r",.'\":;?.")
    if symbolRe.match(allCharList[0]):
        del allCharList[0]
    if symbolRe.match(allCharList[len(allCharList)-1]):
        del allCharList[len(allCharList)-1]
    originalChars = ""
    for aChar in allCharList:
        originalChars = originalChars + " " + aChar
    return originalChars

def FilterSymbol(textcontent):
    tmptext = unicode(textcontent, 'gbk')
    sys.stdout.write("Current text : " + tmptext + "\n")
    #make list first for all Chinese and English
    stringUnits = tmptext.split(" ")
    newtext = ""
    for aString in stringUnits:
        aString = ChompDoubleSideSymbol(aString)
        if re.match(r"^[a-zA-Z]", aString):
            newtext = newtext + " " + aString
        else:
            hanziRe = re.compile(u"[\u4e00-\u9fa5 0-9]")
            if hanziRe.match(aString):
                candidates = hanziRe.findall(aString)
                #process single hanzi
                currHanzi = ""
                for aChar in candidates:
                    currHanzi = currHanzi + " " + aChar
                newtext = newtext + " " + currHanzi
    return newtext


if __name__ == "__main__":
    file_list = ""
    kaldi_scp_file = ""
    if len(sys.argv) >= 3:
        file_list = sys.argv[1]
        kaldi_scp_file = sys.argv[2]
        if not check_file_or_dir(in_param=file_list):
            exit(-1)

    file_list_fp = codecs.open(file_list, "r", "mbcs")
    kaldi_scp_fp = codecs.open(kaldi_scp_file, "w", "mbcs")
    file_array = file_list_fp.readlines()
    scp_index = 0
    for a_file in file_array:
        clean_name = a_file.strip(" \r\n\t")
        file_name = get_filename_from_longdir(long_dir=clean_name)
        file_base_name = os.path.splitext(file_name)[0][0:]
        new_file_name_id = file_base_name + make_standard_index_format("", scp_index)
        kaldi_scp_fp.write(new_file_name_id + "    " + a_file)
        scp_index += 1
    file_list_fp.close()
    kaldi_scp_fp.close()




