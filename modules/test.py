import os
 
root_dir = 'C:/SGM_AI/42Brick/img_human_filter' # 디렉토리
 
img_path_list = []
for (root, dirs, files) in os.walk(root_dir):
    if len(files) > 0:
        for file_name in files:
            if os.path.splitext(file_name)[1] == '.jpg':
                img_path = root + '/' + file_name
                
                img_path = img_path.replace('\\', '/')
                img_path_list.append(img_path)