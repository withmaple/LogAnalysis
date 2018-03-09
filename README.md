# LogAnalysis

通过LogAnalysis.py对指定文件夹中所有log，按照excel中的规则进行自动分析
a)	获取手机中log文件
b)	获取指定目录下所有待分析的log文件
c)	获取指定keyword文件
d)	按照规则获取log中所需信息
i.	只有keyword1&2，搜索log中包含keyword的行，输出到filter_pkgname.log
ii.	有jsonkeyword，填写json对应字段中的值到excel中，最多取前4个值
e)	对于有compare数据的json字段，只要compare with json_keyword包含在jsonout1中，就判断为T，否则为F，结果输出在compare result中
f)	按照c~e的方法循环处理指定目录下所有待分析的log
g)	一轮处理完成，按回车键，可按照a~f的顺序再次获取并分析log
