#!/usr/bin/env python3
import os
import shlex
import shutil
import sys
import tempfile

OUTPUT_PATH=os.path.join(tempfile.gettempdir(), 'freedict-website')

def exec(command):
    ret = os.system(command)
    if ret:
        print("Error, abborting...")
        sys.exit(9)

def copy_recursively(src, dst):
    for src_dir, _dirs, files in os.walk(src):
        dst_dir = src_dir.replace(src, dst, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file in files:
            src_file = os.path.join(src_dir, file)
            dst_file = os.path.join(dst_dir, file)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.copy2(src_file, dst_dir)

if os.path.exists(OUTPUT_PATH):
    shutil.rmtree(OUTPUT_PATH)

exec('lektor build --output-path ' + OUTPUT_PATH)
exec('git checkout master')
copy_recursively(OUTPUT_PATH, '.')
exec('git status')

for directory, _foo, files in os.walk('.'):
    for file in (os.path.join(directory, f) for f in files if f.endswith('.html')):
        exec('git add %s' % shlex.quote(file))
