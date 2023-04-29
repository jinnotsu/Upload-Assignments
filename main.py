import os
import datetime
import yaml
import codecs
import subprocess
import shutil

with open('paths.yaml', 'r') as yml:  # paths.yamlの読み込み
    yaml_load = yaml.safe_load(yml)
read_path = yaml_load['paths']['assignments-path']  # コピー元フォルダの読み取り
read_folders = os.listdir(read_path)  # コピー元フォルダのリスト化
for folder in read_folders:  # コピー元フォルダの数だけ繰り返す
    print(folder)
    src_path = yaml_load['paths']['assignments-path'] + \
        '/' + folder + '/' + folder + '/' + folder + '.c' # コピー元ファイルの読み取り
    dst_folder = yaml_load['paths']['github-path'] + '/' + folder
    dst_file = dst_folder + '/' + folder + '.c'
    last_modified = os.path.getmtime(src_path) # コピー元ファイルの最終更新日時の取得
    jst_datetime = datetime.datetime.utcfromtimestamp(
        last_modified) + datetime.timedelta(hours=9)
    git_date = jst_datetime.strftime('%a %b %d %H:%M:%S %Y +0900')
    if not os.path.exists(dst_folder): # コピー先フォルダが存在しない場合は作成、ファイルのコピー
        os.makedirs(dst_folder)
        shutil.copy(src_path, dst_folder)
        with codecs.open(dst_file, 'r', 'shift_jis') as f:
            content = f.read()
            with codecs.open(dst_file, 'w', 'utf-8') as f_out:
                f_out.write(content)
    dir = os.getcwd()
    os.chdir(yaml_load['paths']['github-path']) # コピー先フォルダにプロンプト移動
    commit_file = folder + '/' + folder + '.c'
    if os.path.isfile(commit_file): #git add, commit
        print('file exists')
    subprocess.run(['git', 'add', commit_file])
    subprocess.run(['git', 'commit', '-m', folder, '--date', git_date])
    os.chdir(dir)
