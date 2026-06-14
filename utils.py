import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


# 导入聊天模型的提示词功能
from langchain_core.prompts import ChatPromptTemplate
# 导入聊天模型的接口
from langchain_deepseek import ChatDeepSeek
# 导入维基百科的搜索引擎
from langchain_community.utilities import WikipediaAPIWrapper


#对这个模型进行封装，定义标题，时长，创造力和api密钥
def generate_script(subject,video_length,creativity,api_key):
    # 从AI获得标题的提示模板
    title_template=ChatPromptTemplate.from_messages(
        [
            ("human","请为{subject}这个主题的视频想一个吸引人的标题")
        ]
    )
    # 从AI获得脚本的提示模板
    script_template=ChatPromptTemplate.from_messages(
        [
            ("human",
             """你是一位短视频博主。根据以下标题和参考信息创作视频脚本。
            视频标题：{title}，视频时长：{duration}分钟。
            要求：开头抓眼球、中间讲干货、结尾留惊喜，格式严格按照【开头、中间、结尾】划分。
            风格轻松年轻化，参考资料仅作辅助：
            ```{wikipedia_search}```""")
        ]
    )
    # 传入用户的API密钥和用户选择的的创造力
    model = ChatDeepSeek(
        api_key=api_key,  # 修正：正确的参数名是 api_key
        model="deepseek-chat",  # 必须填写，必填参数
        temperature=creativity,
        timeout=60
    )
    # 获得标题
    title_chain=title_template|model
    # 获得脚本
    script_chain=script_template|model
    title=title_chain.invoke({"subject":subject}).content

    search= WikipediaAPIWrapper(lang="zh")
    search_result=search.run(subject)

    script=script_chain.invoke({"title":title,"duration":video_length,
                                "wikipedia_search":search_result}).content
    return search_result,title,script
