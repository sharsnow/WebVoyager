# WebVoyager
## github網址  
https://github.com/sharsnow/WebVoyager/tree/RAG

## AI agnet 操作

python .\main.py  --api_key "API_KEY" --api_model gpt-4o --max_iter 10

## 主題
**旅遊小助手**

1. 幫助旅客尋找合適的飯店
2. 尋找旅客適合的景點
3. 提供當地的天氣預報

## 更新後主要使用到的目錄

my_project/  
├── output/  
├── RAG/  
│   ├── __init__.py   
│   ├── chroma_db/  
│   ├── booking_screenshot.png  
│   ├── booking_screenshot2.png  
│   ├── travel_screenshot1.png  
│   ├── travel_screenshot2.png  
│   ├── weather_screenshot.png  
│   ├── visual_descriptions.md  
│   ├── instruction_manual.pdf
│   ├── instruction_manual_generator.py  
│   └── rag_processor.py  
├── main.py  
└── run.py   


---

## 新增內容 (RAG)
- 新增操作手冊(pdf)
- 將RAG生成後的資料放入chroma_db

添加output放置有關RAG產生後的資料  
- instruction_manual.md
    - 經過instruction_manual.pdf產生出的markdown內容並以#, ##, 序號, 圖片描述等資訊
    - 後續可供agent產生流程步驟
- instruction_manual_enhanced.md
    - 將instruction_manual.md的內容轉換成流程步驟
    - 透過此方式可讓agent在執行時，可以根據此內容，較不會產生錯覺
    - 圖片會在做進一步處理，以便產生更詳細的敘述

添加RAG資料夾主要負責處理有關RAG相關的操作
- visual_descriptions.md  
   人工撰寫手冊   
- chroma_db/
    RAG產生後的結果
- .png
    給visual_descriptions.md來了解畫面樣式說明
- instruction_manual_generator
    根據檢索結果生成清楚的行動步驟或答案
- rag_processor
    從知識庫中檢索visual_descriptions.md  
    處理資料的向量化、索引、相似度搜尋（RAG 流程）  
    把檢索到的相關資訊傳遞instruction_manual_generator  

提取並保存如下 Metadata 提高檢索精度至agent.log保存    
- 任務目標 (Task Goal)：   
    - 查詢 5 月 15 日高雄市的天氣。  
- 檢索結果 (Manual Retrieval Results)：  
    - 找到的內容來自 visual_descriptions.md，包括以下操作指引：  
- 操作步驟 (Steps):   
    1. 開啟網頁瀏覽器並前往提供台灣城市天氣資訊的網站。  
    2. 找到搜尋欄或地區選擇下拉選單。
    3. 選擇或輸入「高雄市」作為目標地點。
    4. 使用網站的行事曆功能選擇日期「5 月 15 日」。
    5. 點擊搜尋或提交按鈕，查詢高雄市 5 月 15 日的天氣。
    6. 查看結果，獲取該天的溫度、濕度、降雨機率以及任何天氣警示。
- 最終回答 (Answer):
    - 高雄市 5 月 15 日的天氣為: 白天氣溫 26-32°C，晚上氣溫 27-30°C。

---
## 修改內容 

### main.py
將生成的RAG的內容加入至prompt，以便在進行生成指令及操作步驟會產生符合需求的結果。
`rag_results = search_rag(query=task['ques'], api_key=args.api_key,logger=task_logger)
    manual = generate_instruction_manual(api_key=args.api_key,
                                            task_goal=task['ques'], filtered_results=rag_results, logger=task_logger,
                                            instruction_format="text_steps")`

---
## 測試結果

### visual_description.md

經由`visual_description.md`人工撰寫，由於步驟敘述較為完整儘管在圖片描述上較為影響，在測試結果較為良好

### 以pdf產生markdown內容

經由pdf透過agent產生的markdown無法完全注意到所以細節或是內容，儘管圖片上較清楚，但在測試的結果較容易產生誤差，且耗費的token也較多儘管只有第一次產生內容時才會計算

### 結論

儘管在"以PDF產生markdown內容"的效果沒有如期地好，但是增加RAG比未使用的結果來說更優秀，在不使用RAG需要透過gpt-4o才能達到使用RAG + gpt-4o-mini的效果，花費的token也較低。  

透過"以PDF產生markdown內容"的`instruction_manual_enhanced.md`或許需要人進行校對或修改以更能增加準確度。  