import time
from tools import tools_map
from prompt import gen_prompt, user_prompt
from model_provider import ModelProvider
from dotenv import load_dotenv
from visual_perception import VisualPerceptionModule
from web_actions import WebActions

load_dotenv()


class UIAutomationSystem:
    def __init__(self, url):
        self.mp = ModelProvider()
        self.visual_module = VisualPerceptionModule()
        self.web_actions = WebActions(url)
        self.max_attempts = 10

    def parse_thoughts(self, response):
        try:
            thoughts = response.get("thoughts", {})
            observation = response.get("observation", "")
            plan = thoughts.get("plan", "")
            reasoning = thoughts.get("reasoning", "")
            criticism = thoughts.get("criticism", "")
            prompt = f"plan: {plan}\nreasoning: {reasoning}\ncriticism: {criticism}\nobservation: {observation}"
            return prompt
        except Exception as e:
            print(f"parse_thoughts error: {e}")
            return str(e)

    def agent_execute(self, query):
        cur_attempt = 0
        chat_history = []
        agent_scratch = ""

        while cur_attempt < self.max_attempts:
            cur_attempt += 1
            prompt = gen_prompt(query, agent_scratch)

            print(f'********* {cur_attempt}.开始调用大模型.....')
            response = self.mp.chat(prompt, chat_history)
            print(f'结束调用{cur_attempt}次')

            if not response or not isinstance(response, dict):
                print(f"call llm exception, response is: {response}")
                continue

            action_info = response.get("action", {})
            action_name = action_info.get("name")
            action_args = action_info.get("args", {})
            print(f"当前action_name: {action_name} || action_入参: {action_args}")

            thoughts = response.get("thoughts", {})
            print(f"plan: {thoughts.get('plan')}")
            print(f"reasoning: {thoughts.get('reasoning')}")
            print(f"criticism: {thoughts.get('criticism')}")
            print(f"observation: {thoughts.get('speak')}")

            if action_name == "finish":
                final_answer = action_args.get("answer")
                print(f"final_answer: {final_answer}")
                break

            try:
                func = tools_map.get(action_name)
                if func:
                    call_function_result = func(self.web_actions, self.visual_module, **action_args)
                else:
                    raise ValueError(f"Unknown action: {action_name}")
            except Exception as e:
                print(f"调用工具异常: {e}")
                call_function_result = str(e)

            agent_scratch += f"\nobservation: {response.get('observation', '')}\nexecute action result: {call_function_result}"
            assistant_msg = self.parse_thoughts(response)
            chat_history.append([user_prompt, assistant_msg])

        if cur_attempt == self.max_attempts:
            print("本次任务执行失败!")
        else:
            print("本次任务成功！")


def main():
    url = input("请输入测试网页URL: ")
    system = UIAutomationSystem(url)

    while True:
        query = input("请输入您的测试目标 (输入'exit'退出): ")
        if query.lower() == "exit":
            break
        system.agent_execute(query)


if __name__ == '__main__':
    main()
