import run
import sys
import argparse
import time
import os
import logging
import json
from openai import OpenAI
from prompts import TRAVEL_PROMPT, FORMAT_SETTING_PROMPT, TRAVEL_END_PROMPT



def main():

    parser = argparse.ArgumentParser()
    # parser.add_argument('--test_file', type=str, default='data/test.json')
    parser.add_argument('--max_iter', type=int, default=5)
    parser.add_argument("--api_key", default="key", type=str, help="my-api-key")
    parser.add_argument("--api_model", default="gpt-4-vision-preview", type=str, help="model")
    parser.add_argument("--output_dir", type=str, default='results')
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--max_attached_imgs", type=int, default=1)
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--download_dir", type=str, default="downloads")
    parser.add_argument("--text_only", action='store_true')

    # for web browser
    parser.add_argument("--headless", action='store_true', help='The window of selenium')
    parser.add_argument("--save_accessibility_tree", action='store_true')
    parser.add_argument("--force_device_scale", action='store_true')
    parser.add_argument("--window_width", type=int, default=1024)
    parser.add_argument("--window_height", type=int, default=768)  # for headless mode, there is no address bar
    parser.add_argument("--fix_box_color", action='store_true')

    args = parser.parse_args()

    # OpenAI client
    client = OpenAI(api_key=args.api_key)
    options = run.driver_config(args)

    # Save Result file
    current_time = time.strftime("%Y%m%d_%H_%M_%S", time.localtime())
    result_dir = os.path.join(args.output_dir, current_time)
    os.makedirs(result_dir, exist_ok=True)

    # message 設定
    messages = [{'role': 'system', 'content': TRAVEL_PROMPT}]
    openai_response = client.chat.completions.create(
                    model=args.api_model, messages=messages, max_tokens=1000, seed=args.seed, timeout=30
                )
    # 取得GPT 回應
    
    gpt_4v_res = openai_response.choices[0].message.content
    
    while True: 

        # user 詢問
        user_input = input(gpt_4v_res)
        if user_input == "0": break
        user_input += FORMAT_SETTING_PROMPT #轉換格式

        curr_msg = {'role': 'user', 'content': user_input}
        messages.append(curr_msg)
        openai_response = client.chat.completions.create(
                    model=args.api_model, messages=messages, max_tokens=1000, seed=args.seed, timeout=30
                )
        reply = openai_response.choices[0].message.content

        
        curr_msg = {'role': 'user', 'content': reply}
        messages.append(curr_msg) #轉換格式
         # 轉換成list 格式
        tasks = [json.loads(line) for line in reply.strip().split("\n")]
        
        current_time = time.strftime("%Y%m%d_%H_%M_%S", time.localtime())
        result_dir = os.path.join(args.output_dir, current_time)
        os.makedirs(result_dir, exist_ok=True)
        msg = [] #紀錄本次的回覆
        print("---------------waiting for search...--------------------------")
        for task_id in range(len(tasks)): # 逐一處理每個task
            task = tasks[task_id]
            task_dir = os.path.join(result_dir, 'task{}'.format(task["id"]))
            os.makedirs(task_dir, exist_ok=True)
            run.setup_logger(task_dir)
            logging.info(f'########## TASK{task["id"]} ##########')

            # WebVoyager 尋找資料
            reply = run.get_web_request(task, task_dir, args, client)
            print(reply[-1]["content"])
            messages.append({'role': 'assistant', 'content': reply[-1]["content"]})
            msg.append({'role': 'assistant', 'content': reply[-1]["content"]})
        msg.append({'role': 'system', 'content': TRAVEL_END_PROMPT})
        # 結束本次的詢問
        openai_response = client.chat.completions.create(
                    model=args.api_model, messages=msg, max_tokens=1000, seed=args.seed, timeout=30
                )
        gpt_4v_res = openai_response.choices[0].message.content
        print("-----------------------------------------------------------------")


if __name__ == "__main__":
    # run.main(sys.argv[1:])
    
    main()
    print('End of main')