import json
import os

def _get_workdir_root():
    workdir_root = os.environ.get('WORKDIR_ROOT', "./data/ui_test_results")
    return workdir_root

WORKDIR_ROOT = _get_workdir_root()

def read_file(filename):
    filename = os.path.join(WORKDIR_ROOT, filename)
    if not os.path.exists(filename):
        return f"{filename} not exist, please check file exist before read"
    with open(filename, 'r', encoding="utf-8") as f:
        return "\n".join(f.readlines())

def write_to_file(filename, content):
    filename = os.path.join(WORKDIR_ROOT, filename)
    if not os.path.exists(WORKDIR_ROOT):
        os.makedirs(WORKDIR_ROOT)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    return "write content to file success."

def click_element(web_actions, visual_module, element_text):
    screenshot = web_actions.screenshot()
    element_location = visual_module.locate_element(screenshot, element_text)
    if element_location:
        web_actions.click(element_location['x'], element_location['y'])
        return f"Clicked element with text: {element_text}"
    else:
        return f"Element with text '{element_text}' not found"

def input_text(web_actions, visual_module, element_text, input_value):
    screenshot = web_actions.screenshot()
    element_location = visual_module.locate_element(screenshot, element_text)
    if element_location:
        web_actions.click(element_location['x'], element_location['y'])
        web_actions.input_text(input_value)
        return f"Input '{input_value}' into element with text: {element_text}"
    else:
        return f"Element with text '{element_text}' not found"

def verify_element_exists(web_actions, visual_module, element_text):
    screenshot = web_actions.screenshot()
    element_location = visual_module.locate_element(screenshot, element_text)
    if element_location:
        return f"Element with text '{element_text}' exists"
    else:
        return f"Element with text '{element_text}' not found"

tools_info = [
    {
        "name": "click_element",
        "description": "Click on a web element identified by its text",
        "args": [
            {
                "name": "element_text",
                "type": "string",
                "description": "Text of the element to click"
            }
        ]
    },
    {
        "name": "input_text",
        "description": "Input text into a web element identified by its label or placeholder text",
        "args": [
            {
                "name": "element_text",
                "type": "string",
                "description": "Text of the element to input into"
            },
            {
                "name": "input_value",
                "type": "string",
                "description": "Text to input"
            }
        ]
    },
    {
        "name": "verify_element_exists",
        "description": "Verify if an element with specific text exists on the page",
        "args": [
            {
                "name": "element_text",
                "type": "string",
                "description": "Text of the element to verify"
            }
        ]
    },
    {
        "name": "read_file",
        "description": "Read content from a file",
        "args": [
            {
                "name": "filename",
                "type": "string",
                "description": "Name of the file to read"
            }
        ]
    },
    {
        "name": "write_to_file",
        "description": "Write content to a file",
        "args": [
            {
                "name": "filename",
                "type": "string",
                "description": "Name of the file to write"
            },
            {
                "name": "content",
                "type": "string",
                "description": "Content to write to the file"
            }
        ]
    },
    {
        "name": "finish",
        "description": "完成测试任务",
        "args": [
            {
                "name": "answer",
                "type": "string",
                "description": "测试结果总结"
            }
        ]
    }
]

tools_map = {
    "click_element": click_element,
    "input_text": input_text,
    "verify_element_exists": verify_element_exists,
    "read_file": read_file,
    "write_to_file": write_to_file
}

def gen_tools_desc():
    tools_desc = []
    for idx, t in enumerate(tools_info):
        args_desc = []
        for info in t["args"]:
            args_desc.append({
                "name": info["name"],
                "description": info["description"],
                "type": info["type"]
            })
        args_desc = json.dumps(args_desc, ensure_ascii=False)
        tool_desc = f"{idx+1}.{t['name']}:{t['description']}, args: {args_desc}"
        tools_desc.append(tool_desc)
    tools_prompt = "\n".join(tools_desc)
    return tools_prompt