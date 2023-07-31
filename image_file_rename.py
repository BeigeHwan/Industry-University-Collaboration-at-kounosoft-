import os 
# 시작시 매개변수 
import sys 
# 파일 복사
import shutil
# 문자열 매칭 
import re
import time

        
#def read_all_file(source_directory, dest_directory, pLux=-1, pOcc=-1):
def read_all_file(source_directory, dest_directory):
    output = os.listdir(source_directory)
    source_directory_list=[]
    source_file_list=[]
    dest_directory_list=[]
    dest_file_list=[]
    f_collect = 0    # 수집방식
    f_frontback = 0  # 앞면/후면
    f_screening = 0  # 가림
    f_lux = 0        # 조도
    f_camAngle = 0   # 카메라 각도
    f_turnTable = 0  # 턴테이블 각도 
    f_seq = 0  # 동일한 포즈일 경우 파일 이름 sequence 되어질 부분    
 
    
    
    v_collect = 0    # 수집방법 : 직접촬영(0), 크롤링(1), 데이터구매(2), 기타(3), Crawling 에서 이 부분 수정  
    v_seq = 0        # 동일한 포즈일 경우 파일 이름 sequence 되어질 부분    
    v_lux = 0        # 조도값을 디렉토리에서 추출 
    v_frontback = 0 
    v_screening = 0 
    
    for i in output:
        if os.path.isfile(source_directory + "/" + i):
            if i.endswith('.jpg'):
                source_directory_list.append(source_directory + "/" + i)
                source_file_list.append(i)
                dest_directory_list.append(dest_directory + "/" + i)
                dest_file_list.append(i)
            if i.endswith('.JPG'):
                source_directory_list.append(source_directory + "/" + i)
                source_file_list.append(i)
                dest_directory_list.append(dest_directory + "/" + i)
                dest_file_list.append(i)    
    
    print("completed jpg file list")            
    
    #source_directory2 = "D:\RAW_Image\이미용품\면도기 카트리지 도루코 페이스4 케이스 B\100_001_5V24H"
    
    # 분리된 문자열 
    dir_split_01 = source_directory.split(os.path.sep)
    dir_split_02 = source_directory.split('/')
    
    if len(dir_split_02) > len(dir_split_01) :
        print("dir_split_02")
        size_split = len(dir_split_02) - 1  # split 되어진 디렉토리 명의 길이에서 -1 번째 (조명)
        if size_split > 0:
            tmpStr = dir_split_02[size_split]
            v_lux = int(tmpStr[0:3])
            print("Lux = ", v_lux)  # 조명값 추출
            if tmpStr.find("_CW") > 0:   # Crawling 에서 수정, 크롤링으로 수집되었을 경우
                v_collect = 1
            if tmpStr.find("_MO") > 0:   # Crawling 에서 수정, Mobile로 수집되었을 경우 
                v_collect = 3
        else :
            print("lux value : error")
            exit()
        
        size_split2 = len(dir_split_02) - 2   # split 되어진 디렉토리 명의 길이에서 -2 번째 (제품명)
        if size_split2 > 0:
            tmpStr = dir_split_02[size_split2] 
        #    sizeEnd =len(tmpStr)
        #    match_B = tmpStr[sizeEnd-1]
            #if match_B == "B":
            if tmpStr.find("_B") > 0:   # Crawling 에서 수정 
                v_frontback = 1
            
            elif tmpStr.find("_C") > 0:   # Crawling 에서 수정
                v_frontback = 2

            else:     
                v_frontback = 0
            print(v_frontback)  # 일반/후면   
            
            # 가림 여부 
            if tmpStr.find("포장") > 0:
                v_screening = 1
            elif tmpStr.find("비닐") > 0 :
                v_screening = 2
            elif tmpStr.find("가림") > 0 :
                v_screening = 3
            else: 
                v_screening = 0  
        else :
            print("front/back : error")
            exit()            
        #dir_split_02(size_split).find("")
        #for mi in size_split: 
    else:
        print("dir_split_01")
        size_split = len(dir_split_01) - 1  # split 되어진 디렉토리 명의 길이에서 -1 번째 (조명)
        if size_split > 0:
            tmpStr = dir_split_01[size_split]
            v_lux = int(tmpStr[0:3])
            print("Lux = ", v_lux)  # 조명값 추출
            if tmpStr.find("_CW") > 0:   # Crawling 에서 수정, 크롤링으로 수집되었을 경우
                v_collect = 1
            if tmpStr.find("_MO") > 0:   # Crawling 에서 수정, Mobile로 수집되었을 경우 
                v_collect = 3
        else :
            print("lux value : error")
            exit()
        
        size_split1 = len(dir_split_01) - 2   # split 되어진 디렉토리 명의 길이에서 -2 번째 (제품명)
        if size_split1 > 0:
            tmpStr = dir_split_01[size_split1] 
            sizeEnd =len(tmpStr)
            match_B = tmpStr[sizeEnd-1]
            match_underBar = tmpStr[sizeEnd-2]
            if match_B == "B" and match_underBar == "_":
                v_frontback = 1
            
            elif match_B == "C" and match_underBar == "_":
                v_frontback = 2
            
          #  if tmpStr.find("_B") > 0:   # Crawling 에서 수정 
          #      v_frontback = 1
            else:     
                v_frontback = 0
            print(v_frontback)  # 일반/후면   
            
            # 가림 여부 
            if tmpStr.find("포장") > 0:
                v_screening = 1
            elif tmpStr.find("비닐") > 0 :
                v_screening = 2
            elif tmpStr.find("가림") > 0 :
                v_screening = 3
            else: 
                v_screening = 0  
        else :
            print("front/back : error")
            exit()            
    
    # file copy & make 
    if not os.path.exists(dest_directory):
        os.makedirs(dest_directory)
        
    
    for i in range(len(source_directory_list)):
        shutil.copy2(source_directory_list[i], dest_directory_list[i])
        time.sleep(0.01)
        print("finished copy file " + str(source_directory_list[i]) + "  ==> " + str(dest_directory_list[i]))
        
    # file name -> change   
    idx_cnt = 0
    print("file_list len =" , len(dest_file_list) )
    for idx_name in dest_file_list:  ## os.listdir(dest_directory):
        tmp_fName = idx_name      
        tmp_trunTable = tmp_fName[8:11]
        tmp_camAngle = tmp_fName[1]
        
        i_fname_size = len(tmp_fName)
        
        if i_fname_size > 15 :
            v_seq = tmp_fName[12:15]
        else : 
            v_seq = '0'

        val_trunTable = (int(tmp_trunTable) - 1) * 30
        
        val_camAngle = 0  #default 
        if  tmp_camAngle == "1" :
            val_camAngle = 90
        elif tmp_camAngle == "2" :
            val_camAngle = 70
        elif tmp_camAngle == "3" :
            val_camAngle = 45
        elif tmp_camAngle == "4" :
            val_camAngle = 20
        elif tmp_camAngle == "5" :
            val_camAngle = 0
        else:
            continue
        # {턴테이블각도}_{카메라각도}_{조도}_{가림여부}.jpg
        # 025_060_1000_0.jpg
        f_turnTable = '{0:03d}'.format(val_trunTable)
        f_camAngle = '{0:03d}'.format(val_camAngle)
        f_seq =  '{0:03d}'.format(int(v_seq))
        
        #수집방식, 일반/후면, 가림상태, 조도 
        f_collect ='{0:01d}'.format(v_collect)
        f_frontback = '{0:01d}'.format(v_frontback)
        f_screening = '{0:01d}'.format(v_screening)
        f_lux = '{0:03d}'.format(v_lux)

        full_file_rename = str(f_collect) + str(f_frontback) + str(f_screening) + "_"  \
                           + str(f_lux) + "_" + str(f_camAngle) + "_" + str(f_turnTable) + "_" + str(f_seq) + ".jpg"
        os.rename(dest_directory_list[idx_cnt],  dest_directory + "/" + full_file_rename)
        idx_cnt = idx_cnt + 1
        

