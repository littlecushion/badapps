#coding=utf-8
import sys
reload(sys)
#python默认环境编码时ascii
sys.setdefaultencoding("utf-8")
import subprocess
import os
from console import views

app_id =sys.argv[1]
# app_id = appid
url=get_undownloaded_url(app_id)
downloading(url)
update_database(app_id)    

subprocess.call("python D:\\apptest\\appAutoTest\\monkeyRunner\\aaptOutput.py",shell=True)
subprocess.call("python D:\\apptest\\appAutoTest\\monkeyRunner\\startMonkeyRunner.py",shell=True)
files = os.listdir('D:\\apptest\\appAutoTest\\monkeyRunner\\snapshot')
images= os.listdir('D:\\apptest\\appAutoTest\\monkeyRunner\\snapshot\\'+files[0])

img=''
for i in range(len(images)):
	img=img+images[i]+' '
    # capture%d.png '%(i,)
    
print img
subprocess.call("cd D:\\apptest\\appAutoTest\\monkeyRunner\\snapshot\\"+files[0]+"&& FineCmd.exe "+img+"/lang Mixed /out D:\\apptest\\appAutoTest\\temp\\result.txt /quit",shell=True)
# subprocess.call("python D:\\appdetect\\console\\re.py result.txt "+app_id,shell=True)
reDetect("result.txt",app_id)




# def main():
	# app_id =sys.argv[1]
 #    # app_id = appid
	# url=get_undownloaded_url(app_id)
	# downloading(url)
	# update_database(app_id)    

	# subprocess.call("python D:\\apptest\\appAutoTest\\monkeyRunner\\aaptOutput.py",shell=True)
	# subprocess.call("python D:\\apptest\\appAutoTest\\monkeyRunner\\startMonkeyRunner.py",shell=True)
	# files = os.listdir('D:\\apptest\\appAutoTest\\monkeyRunner\\snapshot')
	# images= os.listdir('D:\\apptest\\appAutoTest\\monkeyRunner\\snapshot\\'+files[0])

	# img=''
	# for i in range(len(images)):
	# 	img=img+images[i]+' '
 #      # capture%d.png '%(i,)
    
	# print img
	# subprocess.call("cd D:\\apptest\\appAutoTest\\monkeyRunner\\snapshot\\"+files[0]+"&& FineCmd.exe "+img+"/lang Mixed /out D:\\apptest\\appAutoTest\\temp\\result.txt /quit",shell=True)
	# # subprocess.call("python D:\\appdetect\\console\\re.py result.txt "+app_id,shell=True)
	# reDetect("result.txt",app_id)



	# subprocess.call("python D:\\apptest\\appAutoTest\\monkeyRunner\\aaptOutput.py",shell=True)
	# subprocess.call("python D:\\apptest\\appAutoTest\\monkeyRunner\\startMonkeyRunner.py",shell=True)
	# files = os.listdir('D:\\apptest\\appAutoTest\\monkeyRunner\\snapshot')
	# images= os.listdir('D:\\apptest\\appAutoTest\\monkeyRunner\\snapshot\\'+files[0])

	# img=''
	# for i in range(len(images)):
	# 	img=img+images[i]+' '
	# 	# capture%d.png '%(i,)
    
	# print img
	# subprocess.call("cd D:\\apptest\\appAutoTest\\monkeyRunner\\snapshot\\"+files[0]+"&& FineCmd.exe "+img+"/lang Mixed /out D:\\apptest\\appAutoTest\\temp\\result.txt /quit",shell=True)
	#subprocess.call("python D:\\appdetect\\console\\re.py result.txt "+app_id,shell=True)

# if __name__ == '__main__':
# 	main()