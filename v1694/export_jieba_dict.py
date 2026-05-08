import jieba.posseg as pseg
from pypinyin import pinyin, Style
import json

# 映射表
TAG_MAP = {
    'n': '名', 'v': '动', 'a': '形', 'r': '代', 'm': '数', 
    'q': '量', 'd': '副', 'c': '连', 'p': '介', 'u': '助', 
    'e': '感', 'y': '感', 'o': '拟', 'i': '名'
}

print("🚀 正在从内存提取词库并计算拼音...")

try:
    # 强制触发加载
    pseg.lcut("初始化")
    
    # 使用你之前跑通的内存访问法
    raw_dict = pseg.dt.word_tag_tab
    
    export_data = {}
    
    count = 0
    total = len(raw_dict)
    
    for word, tag in raw_dict.items():
        if tag:
            # 获取词性映射
            label = TAG_MAP.get(tag[0])
            if label:
                # 计算拼音 (无声调)
                py_raw = pinyin(word, style=Style.NORMAL)
                py_str = "".join([item[0] for item in py_raw])
                
                # 存储为列表：[词性, 拼音]
                export_data[word] = [label, py_str]
        
        count += 1
        if count % 50000 == 0:
            print(f"进度: {count}/{total}")

    # 导出文件
    with open('jieba_dict.js', 'w', encoding='utf-8') as f:
        f.write("window.LOCAL_ASSETS = ")
        json.dump(export_data, f, ensure_ascii=False, separators=(',', ':'))
        f.write(";")
    
    print(f"✨ 成功！生成的词库包含 {len(export_data)} 个词条。")
    print("文件已保存为: jieba_dict.js")

except Exception as e:
    print(f"❌ 出错: {e}")