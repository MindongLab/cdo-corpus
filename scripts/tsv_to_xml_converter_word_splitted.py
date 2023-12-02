from lxml import etree
import pandas as pd
import re  # 导入正则表达式模块

def parse_language_tag(word):
    # 解析词汇中的语言标记，并返回相应的Iso639代码
    lan_match = re.search(r"<lan=(\w+)>", word)
    if lan_match:
        lang_code = lan_match.group(1)
        if len(lang_code) == 2:
            return {"Iso639-1": lang_code, "Iso639-3": "", "Iso639-6": ""}
        elif len(lang_code) == 3:
            return {"Iso639-1": "", "Iso639-3": lang_code, "Iso639-6": ""}
        elif len(lang_code) == 4:
            return {"Iso639-1": "", "Iso639-3": "", "Iso639-6": lang_code}
    return {}

# 添加一个检测标点的函数
def is_punctuation(text):
    # 包含所有需要检测的标点符号
    punctuation_list = [",", ".", "...", ":", ";", "!", "?", "?!", "!?", "(", ")", "“", "”", "，", "。", "！", "（", "）", "……", "…", "？！", "！？"]
    return text in punctuation_list

# 添加函数解析 <typofix=> 标签
def parse_typofix_tag(word):
    match = re.search(r"<typofix=([^>]+)>", word)
    return {"TypoFix": match.group(1)} if match else {}

# 添加函数解析 <y=> 标签
def parse_y_tag(word):
    match = re.search(r"<y=([^>]+)>", word)
    return {"YngPing": match.group(1)} if match else {}

def create_xml_elements_from_tsv_final(row, corpus, providers_added):
    # Common attributes
    provider_name_text = row['Provider']
    speaker_id_text = str(row['Speaker ID'])
    date_text = f"{row['Year']}-{str(row['Month']).zfill(2)}-{str(row['Day']).zfill(2)}"
    time_text = row['HH:MM:SS (UTC+8)']

    # 将年、月、日转换为字符串
    year_str = str(row['Year'])
    month_str = str(row['Month'])
    day_str = str(row['Day'])
    
    # 检查并转换 'Mandarin Trans.' 列的值
    mandarin_trans = row['Mandarin Trans.']
    if pd.isna(mandarin_trans) or not isinstance(mandarin_trans, str):
        mandarin_trans = ""  # 将非字符串或空值转换为空字符串

    # 创建SecLv1元素
    sec_lv1 = etree.SubElement(corpus, "SecLv1", Section="Sentence", Year=year_str, Month=month_str, Day=day_str, Date=date_text, HourMinuteSecond=time_text, Property=row['Property'])
    translation = etree.SubElement(sec_lv1, "Translation", TransText=mandarin_trans, **{"Iso639-1": "zh", "Iso639-3": "cmn"})

    # 在此处添加Speaker和Provider
    speaker = etree.SubElement(sec_lv1, "Speaker")
    speaker_id = etree.SubElement(speaker, "SpeakerId")
    speaker_id.text = speaker_id_text

    provider = etree.SubElement(sec_lv1, "Provider")
    provider_name = etree.SubElement(provider, "Name")
    provider_name.text = provider_name_text

    # 处理每个词汇
    words = row['Mindong'].split()
    for word in words:
        text = word.split('<')[0]  # 提取文本部分
        # 检查是否是标点符号
        if is_punctuation(text):
            # 创建标点符号的 SecLv2 元素
            etree.SubElement(sec_lv1, "SecLv2", Text=text, Section="Punctuation")
        else:
            lang_tags = parse_language_tag(word)
            typofix_tags = parse_typofix_tag(word)
            y_tags = parse_y_tag(word)

            iso_tags = {"Iso639-1": "zh", "Iso639-3": "cdo", "Iso639-6": row['ISO 639-6']}
            iso_tags.update(lang_tags)  # 如果为非闽东语，更新语言标签
            extra_tags = {}
            extra_tags.update(typofix_tags)  # 添加TypoFix属性
            extra_tags.update(y_tags)        # 添加YngPing属性

            # 创建SecLv2元素
            section_type = "Character" if len(text) == 1 else "Word"
            sec_lv2 = etree.SubElement(sec_lv1, "SecLv2", Section=section_type, Text=text, **iso_tags, **extra_tags)

            # 处理翻译
            if '<m=' in word:
                translation_text = re.search(r"<m=([^>]+)>", word).group(1)
                etree.SubElement(sec_lv2, "Translation", TransText=translation_text, **{"Iso639-1": "zh", "Iso639-3": "cmn"})

    return corpus

def convert_tsv_to_xml_final(tsv_file_path):
    tsv_data = pd.read_csv(tsv_file_path, sep='\t')
    ns_map = {"xsi": "http://www.w3.org/2001/XMLSchema-instance"}
    corpus = etree.Element("Corpus", nsmap=ns_map)
    corpus.set("{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation", "cdo-plaintext-corpus-document.xsd")

    providers_added = set()
    for index, row in tsv_data.iterrows():
        create_xml_elements_from_tsv_final(row, corpus, providers_added)

    xml_str = etree.tostring(corpus, pretty_print=True, encoding='UTF-8', xml_declaration=True).decode()

    # 将生成的 XML 写入文件
    output_file_path = tsv_file_path.replace('.tsv', '.xml')
    with open(output_file_path, 'w', encoding='UTF-8') as file:
        file.write(xml_str)

    return xml_str

# 使用
tsv_file_path = 'file_to.tsv'
xml_output_final = convert_tsv_to_xml_final(tsv_file_path)

# 输出结果到命令行
print(xml_output_final)
