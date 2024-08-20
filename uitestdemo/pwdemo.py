from playwright.sync_api import sync_playwright
from paddleocr import PaddleOCR
import time

def click(page, target_text):
    # 对整个页面进行截图
    pic_path = ".../snapshots/00.png"
    page.screenshot(path=pic_path, full_page=True)

    # 初始化PaddleOCR
    ocr = PaddleOCR(use_angle_cls=True, lang="ch")

    # 使用PaddleOCR识别文字
    ocr_result = ocr.ocr(pic_path, cls=True)

    # 遍历识别结果，找到目标文字的坐标
    target_coords = None
    for line in ocr_result:
        for word_info in line:
            # 获取识别结果的文字信息
            textinfo = word_info[1][0]
            print(textinfo)

            if target_text in textinfo:
                # 获取文字的坐标（中心点）
                x1, y1 = word_info[0][0]
                x2, y2 = word_info[0][2]
                target_coords = {"x": (x1 + x2) / 2, "y": (y1 + y2) / 2}
                break
        if target_coords:
            break

    # 点击坐标
    if target_coords:
        page.mouse.click(target_coords["x"], target_coords["y"])
    else:
        print(f"未找到目标文字：{target_text}")

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # 打开本地的 HTML 文件
    page.goto(r"C:\PycharmProjects\uitestAgent\homepage\1.html")

    # 等待10秒，以便观察页面加载
    time.sleep(10)

    # 调用click方法进行文字识别和点击
    click(page, "存在")  # 替换为你要识别和点击的文字
    page.wait_for_timeout(2000)  # 等待2秒

    click(page, "固态物质")  # 替换为你要识别和点击的文字
    page.wait_for_timeout(2000)  # 等待2秒

    click(page, "氧")  # 替换为你要识别和点击的文字
    page.wait_for_timeout(2000)  # 等待2秒

    click(page, "岩石")  # 替换为你要识别和点击的文字
    page.wait_for_timeout(2000)  # 等待2秒

    click(page, "石斧")  # 替换为你要识别和点击的文字
    page.wait_for_timeout(2000)  # 等待2秒

    click(page, "提交")  # 替换为你要识别和点击的文字
    page.wait_for_timeout(2000)  # 等待2秒

    # 关闭浏览器
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)