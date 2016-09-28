Auther:      ZBenBen
Create Date: 2013-12-06


脚本文件说明：
	SmaliAligment.py   :脚本运行文件
	
脚本运行说明：
	命令行运行方式为
	python SmaliAlignment.py -a Android_Smali -c Your_Smali -o Out_Smali
	-a Android的smali目录
	-c Your的smali目录
	-o 最终输出目录(该目录必须为新的，不能已经存在)
	
	目录可以输入绝对地址 如F:\smali\Android_Smali 也可以输入直接输入脚本同目录下的相对地址 如；Android_Smali
	注意：输入的目录结尾不需要加入 \   
	
	脚本会生成log文件Smali_Alignment_Log.txt，里面可以查看每次运行时改动的Your_Smali文件
	
	
VersionInfo：
---------------
	Version: 1.0 (Python Version:3.3.2)
	  Data : 2013-12-06
	   Log : smali自动调整工具建立
---------------
	Version: 1.1 (Python Version:3.3.2)
	  Data : 2013-12-09
	   Log : 修复了对于权限变更后的method调整结果错误的问题
			 修复了对于不含method的smali文件调整后文件为空的问题
---------------
	Version: 1.2 (Python Version:3.3.2)
	  Data : 2013-12-10
	   Log : 修复了某些文件method识别错误导致重复输出method的问题
			 更改了脚本运行交互 
---------------
	Version: 1.3 (Python Version:2.7.6)
	  Data : 2013-12-11
	   Log : 更换python版本为2.7.6
			 更改了脚本运行参数输入方式
			 修复连续空行调整后空行丢失的问题
			 增加改动smali文件Log输出
			 去掉文件oppo.txt和android.txt改为内存存储
			 优化处理速度
---------------
	Version: 1.3.1 (Python Version:2.7.6)
	  Data : 2013-12-14
	   Log : 修复# virtual method 前数据重复的问题