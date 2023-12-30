import os
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove
from enum import Enum

class MetaBlockState:
    SEARCH = 0
    INSIDE = 1
    DONE = 2

# Removes # hashtags from tag blocks in metadata
def fix_tags_block_metadata(file_path):
    if (not file_path.endswith(".md")):
        return

    fh, abs_path = mkstemp()

    with open(file_path, encoding='utf-8') as reader:
        with fdopen(fh,'w', encoding='utf-8') as new_file:
            block_state = MetaBlockState.SEARCH

            for line in reader.readlines():
                if "---" in line:
                    if   (block_state is MetaBlockState.SEARCH):
                        block_state = MetaBlockState.INSIDE
                    elif (block_state is MetaBlockState.INSIDE):
                        block_state = MetaBlockState.DONE

                if block_state is MetaBlockState.INSIDE and "tags:" in line:
                    print("tags block found")
                    line = line.replace("#", "")
                    print(line)
                
                # new_file.write(line)

    #Copy the file permissions from the old file to the new file
    # copymode(file_path, abs_path)
    # #Remove original file
    # remove(file_path)
    # #Move new file
    # move(abs_path, file_path)

# Escapes hashtag usage in content body so they're not picked up as tags
def fix_tags_in_content(file_path):
    if (not file_path.endswith(".md")):
        return

    fh, abs_path = mkstemp()

    file_fixed = False

    with open(file_path, encoding='utf-8') as reader:
        with fdopen(fh,'w', encoding='utf-8') as new_file:
            block_state = MetaBlockState.SEARCH

            for line in reader.readlines():
                if "---" in line:
                    if   (block_state is MetaBlockState.SEARCH):
                        block_state = MetaBlockState.INSIDE
                    elif (block_state is MetaBlockState.INSIDE):
                        block_state = MetaBlockState.DONE

                if block_state is MetaBlockState.DONE and "#" in line:
                    fixed = False
                    line_fix = ""
                    for i in range(len(line)):
                        if (line[i] == '#' and
                            (i==0 or (line[i-1] == "\n" or line[i-1] == " ")) and
                            (i==len(line)-1 or line[i+1].isalpha())):
                            line_fix += "\#"
                            fixed = True
                        else:
                            line_fix += line[i]
                    
                    if fixed:
                        file_fixed = True
                        print("A: " + line)
                        print("B: " + line_fix)
                        line = line_fix
                
                new_file.write(line)
    
    if file_fixed:
        print(file_path)

    #Copy the file permissions from the old file to the new file
    copymode(file_path, abs_path)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)

def fix_youtube_clipping(file_path):
    if (not file_path.endswith("YouTube.md")):
        return

    fh, abs_path = mkstemp()

    with open(file_path, encoding='utf-8') as reader:
        with fdopen(fh,'w', encoding='utf-8') as new_file:
            print(abs_path)
            is_youtube_description = False
            for line in reader.readlines():
                if "Description" in line:
                    if (is_youtube_description == False):
                        print(file_path)
                    is_youtube_description = not is_youtube_description
                    
                if is_youtube_description and "#" in line:
                    fixed = False
                    line_fix = ""
                    for i in range(len(line)):
                        if (line[i] == '#' and
                            (i==0 or (line[i-1] == "\n" or line[i-1] == " ")) and
                            (i==len(line)-1 or line[i+1].isalpha())):
                            line_fix += "\#"
                            fixed = True
                        else:
                            line_fix += line[i]
                    
                    if fixed:
                        print("A: " + line)
                        print("B: " + line_fix)

                    new_file.write(line_fix)
                else:
                    new_file.write(line)

    #Copy the file permissions from the old file to the new file
    copymode(file_path, abs_path)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)



# ==== Main ====

vault_path = 'D:\\obsidian\\EvernoteYarle'
markup_files = []

for root_dirs_files in os.walk(vault_path):
    for y in root_dirs_files[2]:
        if (y.endswith(".md")):
            # print(y)
            markup_files.append(os.path.join(root_dirs_files[0], y))

youtube_tags = []

i = 0
for file_path in markup_files:
    #fix_youtube_clipping

    # fix_tags_block_metadata(file_path)
    fix_tags_in_content(file_path)
    
    i += 1
    # if (i > 100):
    #     break

print("All done!")


