# -*- coding: UTF-8 -*-
import requests

Header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62'}
version_list,WEEKLY_source_list,STABLE_source_list,source_list=[],[],[],[]

r = requests.get('https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/files/xiaomi.eu/MIUI-WEEKLY-RELEASES/',headers=Header).text
r = r[r.find('<tbody>')+8:r.find('</tbody>')]
for i in range(r.count('<th scope="row" headers="files_name_h"><a href="')):
    r = r[r.find('<th scope="row" headers="files_name_h"><a href="')+48:]
    version_list.append('https://sourceforge.net/'+r[:r.find('"')])
    r = r[r.find('</tr>')+5:]

r = requests.get('https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/files/xiaomi.eu/MIUI-STABLE-RELEASES/',headers=Header).text
r = r[r.find('<tbody>')+8:r.find('</tbody>')]
for i in range(r.count('<th scope="row" headers="files_name_h"><a href="')):
    r = r[r.find('<th scope="row" headers="files_name_h"><a href="')+48:]
    version_list.append('https://sourceforge.net/'+r[:r.find('"')])
    r = r[r.find('</tr>')+5:]

versionL,modelL=[],[]

for i in version_list:
    r = requests.get(i,headers=Header).text
    r = r[r.find('<tbody>')+8:r.find('</tbody>')]
    for j in range(r.count('<th scope="row" headers="files_name_h"><a href="')):
        if 'readme.md' in r[r.find('<tr title='):r.find('</tr>')]:
            continue
        r = r[r.find('<th scope="row" headers="files_name_h"><a href="')+48:]
        url = r[:r.find('"')]
        r = r[r.find('<td headers="files_date_h" class="opt"><abbr title="')+52:]
        date = r[:r.find('"')]
        r = r[r.find('<td headers="files_size_h" class="opt">')+39:]
        size = r[:r.find('</td>')]
        file_name = url[:url.rfind('/')][url[:url.rfind('/')].rfind('/')+1:]
        if len(file_name.split('_')) == 5:
            model = file_name.split('_')[2]
            version = file_name.split('_')[3]
        elif len(file_name.split('_')) == 6:
            model = file_name.split('_')[2]+' '+file_name.split('_')[3]
            version = file_name.split('_')[4]
        if not version in versionL and not 'V' in version:
            versionL.append(version)
        elif not version[:version.rfind('.')] in versionL and 'V' in version:
            versionL.append(version[:version.rfind('.')])
        if 'STABLE' in url:
            STABLE_source_list.append([model,version,date,file_name,size,url])
        elif 'WEEKLY' in url:
            WEEKLY_source_list.append([model,version,date,file_name,size,url])
        source_list.append([model,version,date,file_name,size,url])
        r = r[r.find('</tr>')+5:]
    
for i in sorted(STABLE_source_list,key=lambda date: date[2]):
    if not i[0] in modelL:
        modelL.append(i[0])
modelL.reverse()
versionL=sorted(versionL,key=lambda x:tuple(int(v.replace('V','')) for v in x.split(".")),reverse=True)
source_list=sorted(source_list,key=lambda date: date[2],reverse=True)
STABLE_source_list=sorted(STABLE_source_list,key=lambda date: date[2],reverse=True)
WEEKLY_source_list=sorted(WEEKLY_source_list,key=lambda date: date[2],reverse=True)

# version
for i in versionL:
    with open('MiuiEURepository/zh-cn/by-version/'+i+'.md','w',encoding='utf-8') as f:
        f.write('# '+i+'\n')
        f.write('| 机型 | 版本 | 更新日期 | 文件名 | 大小 | 下载链接 |\n| ---- | ---- | ---- | ---- | ---- | ---- |\n')
        for k in modelL:
            for j in source_list:
                if 'V' in i:
                    if j[1][:j[1].rfind('.')] == i and j[0] == k:
                        f.write('| '+j[0]+' | '+j[1]+' | '+j[2]+' | '+j[3]+' | '+j[4]+' | [SourceForge]('+j[5]+') |\n')
                else:
                    if j[1] == i and j[0] == k:
                        f.write('| '+j[0]+' | '+j[1]+' | '+j[2]+' | '+j[3]+' | '+j[4]+' | [SourceForge]('+j[5]+') |\n')
            
# model 
for i in modelL:
    with open('MiuiEURepository/zh-cn/by-model/'+i+'.md','w',encoding='utf-8') as f:
        f.write('# '+i+'\n')
        f.write('## 开发版\n')
        f.write('| 机型 | 版本 | 更新日期 | 文件名 | 大小 | 下载链接 |\n| ---- | ---- | ---- | ---- | ---- | ---- |\n')
        for j in WEEKLY_source_list:
            if j[0] == i:
                f.write('| '+j[0]+' | '+j[1]+' | '+j[2]+' | '+j[3]+' | '+j[4]+' | [SourceForge]('+j[5]+') |\n')
        f.write('## 稳定版\n')
        f.write('| 机型 | 版本 | 更新日期 | 文件名 | 大小 | 下载链接 |\n| ---- | ---- | ---- | ---- | ---- | ---- |\n')
        for j in STABLE_source_list:
            if j[0] == i:
                f.write('| '+j[0]+' | '+j[1]+' | '+j[2]+' | '+j[3]+' | '+j[4]+' | [SourceForge]('+j[5]+') |\n')

# version
for i in versionL:
    with open('MiuiEURepository/en-us/by-version/'+i+'.md','w',encoding='utf-8') as f:
        f.write('# '+i+'\n')
        f.write('| Model | Version | Last Updated | File Name | Size | Download Link |\n| ---- | ---- | ---- | ---- | ---- | ---- |\n')
        for k in modelL:
            for j in source_list:
                if 'V' in i:
                    if j[1][:j[1].rfind('.')] == i and j[0] == k:
                        f.write('| '+j[0]+' | '+j[1]+' | '+j[2]+' | '+j[3]+' | '+j[4]+' | [SourceForge]('+j[5]+') |\n')
                else:
                    if j[1] == i and j[0] == k:
                        f.write('| '+j[0]+' | '+j[1]+' | '+j[2]+' | '+j[3]+' | '+j[4]+' | [SourceForge]('+j[5]+') |\n')
            
# model 
for i in modelL:
    with open('MiuiEURepository/en-us/by-model/'+i+'.md','w',encoding='utf-8') as f:
        f.write('# '+i+'\n')
        f.write('## Weekly\n')
        f.write('| Model | Version | Last Updated | File Name | Size | Download Link |\n| ---- | ---- | ---- | ---- | ---- | ---- |\n')
        for j in WEEKLY_source_list:
            if j[0] == i:
                f.write('| '+j[0]+' | '+j[1]+' | '+j[2]+' | '+j[3]+' | '+j[4]+' | [SourceForge]('+j[5]+') |\n')
        f.write('## Stable\n')
        f.write('| Model | Version | Last Updated | File Name | Size | Download Link |\n| ---- | ---- | ---- | ---- | ---- | ---- |\n')
        for j in STABLE_source_list:
            if j[0] == i:
                f.write('| '+j[0]+' | '+j[1]+' | '+j[2]+' | '+j[3]+' | '+j[4]+' | [SourceForge]('+j[5]+') |\n')

# readme
with open('MiuiEURepository/README.md','w',encoding='utf-8') as f:
    f.write('## A Repository of MIUI EU 一个MIUI EU的收集仓库\n')
    f.write('[English](#Miui-EU-Repository)  [简体中文](#Miui-EU-收集仓库)\n***\n')
    f.write('# Miui EU Repository\n')
    f.write('[Model](#Model)  [Version](#Version)\n')
    f.write('## Model\n')
    f.write('[Xiaomi](#Xiaomi)  [Redmi](#Redmi)  [Others](#Others)\n')
    f.write('### Xiaomi\n')
    f.write('| |\n| ---- | ---- | ---- |\n')
    c=0
    for i in modelL:
        if 'MI' in i or 'XM' in i:
            c+=1
            f.write('| ['+i+'](/en-us/by-model/'+i.replace(' ','%20')+'.md) ')
            if c%3 == 0:
                f.write('|\n')
    f.write(' |'*(c-c%3)+'\n')
    f.write('### Redmi\n')
    f.write('| |\n| ---- | ---- | ---- |\n')
    c=0
    for i in modelL:
        if 'HM' in i:
            c+=1
            f.write('| ['+i+'](/en-us/by-model/'+i.replace(' ','%20')+'.md) ')
            if c%3 == 0:
                f.write('|\n')
    f.write(' |'*(c-c%3)+'\n')
    f.write('### Others\n')
    f.write('| |\n| ---- | ---- | ---- |\n')
    c=0
    for i in modelL:
        if (not 'HM' in i) and (not 'MI' in i) and (not 'XM' in i):
            c+=1
            f.write('| ['+i+'](/en-us/by-model/'+i.replace(' ','%20')+'.md) ')
            if c%3 == 0:
                f.write('|\n')
    f.write(' |'*(c-c%3)+'\n')
    f.write('## Version\n')
    f.write('[Weekly](#Weekly)  [Stable](#Stable)\n')
    f.write('### Weekly\n')
    f.write('| |\n| ---- | ---- | ---- |\n')
    c=0
    for i in versionL:
        if not 'V' in i:
            c+=1
            f.write('| ['+i+'](/en-us/by-version/'+i+'.md) ')
            if c % 3 ==0:
                f.write('|\n')
    f.write(' |'*(c-c%3)+'\n')
    f.write('### Stable\n')
    f.write('| |\n| ---- | ---- | ---- |\n')
    c=0
    for i in versionL:
        if 'V' in i:
            c+=1
            f.write('| ['+i+'](/en-us/by-version/'+i+'.md) ')
            if c % 3 ==0:
                f.write('|\n')
    f.write(' |'*(c-c%3)+'\n')
    f.write('# Miui EU 收集仓库\n')
    f.write('[机型](#机型)  [版本](#版本)\n')
    f.write('## 机型\n')
    f.write('[小米](#小米)  [红米](#红米)  [其它](#其它)\n')
    f.write('### 小米\n')
    f.write('| |\n| ---- | ---- | ---- |\n')
    c=0
    for i in modelL:
        if 'MI' in i or 'XM' in i:
            c+=1
            f.write('| ['+i+'](/zh-cn/by-model/'+i.replace(' ','%20')+'.md) ')
            if c%3 == 0:
                f.write('|\n')
    f.write(' |'*(c-c%3)+'\n')
    f.write('### 红米\n')
    f.write('| |\n| ---- | ---- | ---- |\n')
    c=0
    for i in modelL:
        if 'HM' in i:
            c+=1
            f.write('| ['+i+'](/zh-cn/by-model/'+i.replace(' ','%20')+'.md) ')
            if c%3 == 0:
                f.write('|\n')
    f.write(' |'*(c-c%3)+'\n')
    f.write('### 其它\n')
    f.write('| |\n| ---- | ---- | ---- |\n')
    c=0
    for i in modelL:
        if (not 'HM' in i) and (not 'MI' in i) and (not 'XM' in i):
            c+=1
            f.write('| ['+i+'](/zh-cn/by-model/'+i.replace(' ','%20')+'.md) ')
            if c%3 == 0:
                f.write('|\n')
    f.write(' |'*(c-c%3)+'\n')
    f.write('## 版本\n')
    f.write('[开发版](#开发版)  [稳定版](#稳定版)\n')
    f.write('### 开发版\n')
    f.write('| |\n| ---- | ---- | ---- |\n')
    c=0
    for i in versionL:
        if not 'V' in i:
            c+=1
            f.write('| ['+i+'](/zh-cn/by-version/'+i+'.md) ')
            if c % 3 ==0:
                f.write('|\n')
    f.write(' |'*(c-c%3)+'\n')
    f.write('### 稳定版\n')
    f.write('| |\n| ---- | ---- | ---- |\n')
    c=0
    for i in versionL:
        if 'V' in i:
            c+=1
            f.write('| ['+i+'](/zh-cn/by-version/'+i+'.md) ')
            if c % 3 ==0:
                f.write('|\n')
    f.write(' |'*(c-c%3)+'\n')
