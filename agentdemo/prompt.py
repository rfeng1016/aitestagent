from tools import gen_tools_desc

constraints = [
    "仅使用下面列出的动作",
    "你只能主动行动,在计划行动时需要考虑这一点",
    "你通过WebActions和VisualPerceptionModule与网页交互,不要尝试直接操作DOM或JavaScript"
]

resources = [
    "WebActions模块用于执行网页操作",
    "VisualPerceptionModule用于识别和定位网页元素",
    "你是一个训练有素的UI测试专家,利用你的知识来设计和执行测试用例"
]

best_practices = [
    "在执行操作前,先使用视觉感知模块确认元素位置",
    "每个操作后,验证操作结果",
    "如果操作失败,尝试不同的定位策略或等待页面加载",
    "记录每个测试步骤和结果",
    "优先使用稳定的定位方法,如ID或唯一文本"
]

prompt_template = """
你是一个UI自动化测试专家,你的任务是执行网页UI测试。 

目标:
{query}

限制条件说明:
{constraints}

动作说明:这是你唯一可使用的动作,你的任何操作都必须通过以下操作实现：
{actions}

资源说明:
{resources}

最佳实践的说明:
{best_practices}

agent_scratch:{agent_scratch}

你应该以json格式响应,响应格式如下:
{response_format_prompt}

确保响应结果可以由python json.loads()成功加载。
"""

response_format_prompt = """
{
    "action": {
        "name": "action name",
        "args": {
            "args name": "args value"
        }
    },
    "thoughts":{
        "plan": "简单的描述短期和长期的测试计划",
        "criticism": "对当前测试策略的建设性批评",
        "speak": "当前测试步骤的总结",
        "reasoning": "选择此操作的原因"
    },
    "observation": "观察当前测试进度和结果"
}
"""

action_prompt = gen_tools_desc()
constraints_prompt = "\n".join([f"{idx+1}.{con}" for idx, con in enumerate(constraints)])
resources_prompt = "\n".join([f"{idx+1}.{con}" for idx, con in enumerate(resources)])
best_practices_prompt = "\n".join([f"{idx+1}.{con}" for idx, con in enumerate(best_practices)])

def gen_prompt(query, agent_scratch):
    prompt = prompt_template.format(
        query=query,
        constraints=constraints_prompt,
        actions=action_prompt,
        resources=resources_prompt,
        best_practices=best_practices_prompt,
        agent_scratch=agent_scratch,
        response_format_prompt=response_format_prompt
    )
    return prompt

user_prompt = "根据给定的测试目标和迄今为止的测试进展,确定下一个要执行的测试操作,并使用前面指定的JSON模式进行响应："
