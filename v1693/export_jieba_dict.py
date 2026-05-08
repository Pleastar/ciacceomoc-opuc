import jieba.posseg as pseg
import json

# 1. 定义映射表
TAG_MAP = {
    'n': '名', 'v': '动', 'a': '形', 'r': '代',
    'm': '数', 'q': '量', 'd': '副', 'c': '连',
    'p': '介', 'u': '助', 'e': '感', 'y': '感',
    'o': '拟', 'i': '名'
}

print("正在从内存直接提取 jieba 词典（不经过物理路径，解决报错问题）...")

try:
    # 2. 随便分个词，强制触发 jieba 把词典加载到内存里
    pseg.lcut("初始化内存词典") 
    
    # 3. 直接访问 jieba.posseg 已经在内存里加载好的映射表
    # 这是最稳妥的方法，因为不涉及寻找硬盘上的 dict.txt
    raw_dict = pseg.dt.word_tag_tab
    
    export_dict = {}
    for word, tag in raw_dict.items():
        if tag:
            # 取词性的首字母进行匹配
            label = TAG_MAP.get(tag[0])
            if label:
                export_dict[word] = label

    print(f"✅ 提取成功！共获得 {len(export_dict)} 个有效词条。")

    # 4. 写入 JS 文件
    with open('jieba_dict.js', 'w', encoding='utf-8') as f:
        f.write("window.JIEBA_DICT = ")
        # 紧凑格式写入，减小体积
        json.dump(export_dict, f, ensure_ascii=False, separators=(',', ':'))
        f.write(";")
    
    print("\n[恭喜] 文件夹下应该已经出现了 'jieba_dict.js'。")
    print("现在，请把它和你的 'index.html' 一起上传到 GitHub 仓库根目录。")

except Exception as e:
    print(f"❌ 依然报错: {e}")
    print("提示：如果还报错，请尝试在命令行输入 'pip install --upgrade jieba' 升级一下库。")