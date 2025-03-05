import json
from typing import Iterable

class ManualSearcher:
    def __init__(self, language='zh_CN'):
        self.language = language
        self.localization_file_name = "manual.json"
        self.languages_available = ['zh_CN', 'EN', 'JP', 'zh_TW']

    def _get_localization_file_name(self, language="LanguageNotSelected"):
        if language == 'LanguageNotSelected' or language not in ['EN', 'JP', 'zh_TW']:
            # 未设定语言或语言设定不合法时默认使用中文
            language = self.language
        return f'./localizations/{language}/manual.json'
    
    def _bottom_up_search(self, directory_series):
        # 根据输入地址单找到帮助文档中最接近的项目。地址单结构应为`["command_name", "argument_name", "subargument_name", ...]`

        # 确保地址单为可迭代对象
        if isinstance(directory_series, str):
            directory_series = [directory_series]
        if not isinstance(directory_series, Iterable):
            return "[DebuggingError]Invalid arguments"
        directory_series = list(directory_series)
        directory_series.append('_END') # 在地址单末尾添加标识符以停止搜索
        
        # 尝试从地址单头读取语言。如无，选择默认语言
        lang = self.language
        if directory_series[0] in self.languages_available:
            lang = directory_series[0]

        # 读取本地化文本，初始化搜索范围
        with open(self._get_localization_file_name(language=lang), 'r') as f:
            present_dictionary = json.load(f)
        for directory in directory_series: # 逐级搜索是否有对应下级，若无则返回该级帮助手册。
            if directory in present_dictionary:
                present_dictionary = present_dictionary[directory]
            elif 'manual_text' in present_dictionary:
                return present_dictionary['manual_text']
            else: # 该级无帮助手册时回复未找到帮助手册
                with open(self._get_localization_file_name(language=lang), 'r') as f:
                    return directory.join(json.load(f)['errors']['ManualNotFound'].split('_Skadi'))

    
    def find(self, *args):
        # 输出API。参数格式为`[("language",) "command_name", "argument_name", "subargument_name", ...]`
        if len(args) == 0: # 参数为空时返回空参数错误
            return self._bottom_up_search(['errors', 'FindArgumentEmpty'])
        

        return self._bottom_up_search(args)