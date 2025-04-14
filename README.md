# WebVoyager
## github網址  
https://github.com/sharsnow/WebVoyager/tree/muti-agent  

## AI agnet 操作

python .\main.py  --api_key "API_KEY" --api_model gpt-4o --max_iter 10

## 主題
**旅遊小助手**

1. 幫助旅客尋找合適的飯店
2. 尋找旅客適合的景點
3. 提供當地的天氣預報

## 更改內容(travel-agent update)

在本次的修改中，希望在用戶輸入詢問時，可以根據用戶的需求以及目前agent已知的訊息產生需要的任務目標而非不斷重複相同的資訊。除此之外在上次版本中，在飯店搜尋上準確度十分低，希望透過增加error prompt使WebVoyager可以有不同的策略進行選擇。


### 1. prompt.py  
**新增 ERROR_GROUNDING_AGENT_PROMPT**  
此prompt主要是用來處理當WebVoyager回傳時產生的問題並且提供建議以及分析，讓下次的執行可以更往用戶的需求靠近。  

**新增 SYSTEM_PREVIOUS_STEP**  
用來記錄此task過去的步驟，主要避免agent不斷重複執行相同命令並且希望可以嘗試像button, input, scroll等不同的網頁操作方式。除此之外，為了避免agent過於鑽牛角尖因此增加條件，若是操作步驟位導致有不同的結果或是策略，可以先以網站的預設的方式先前往下個網頁再做更精準的操作或是目的。  

**修改 FORMAT_SETTING_PROMPT**  
本來設定在每次執行都會強迫產生三個任務(hotel search, weather info, tourist attract)但每輪用戶輸入需求時可能會產生的任務需求與前一輪的需求是相同的而導致不必要的浪費。因此增加條件，若是用戶的需求與之前的需求沒變化時則不再產生新的任務需求。  
由於在用戶在尋找飯店的需求上會較多且較為複雜，因此在prompts先假設一定的內容如: 日期、人數及價錢等資訊，以免顧客忘記提供而導致執行上無法產生較為正確的結果。  

**修改 TRAVEL_END_PROMPT**
修改成會強調在本輪的產生的結果避免說明不必要的資訊或是內容  

___
### 2. run.py
填加關於Error ground agent的內容

___
### 3. main.py
- 使頁面為全螢幕
- 重新整理產生資料夾的位置
- 填加travel-agent的在每一輪的interact_messages.json以更好得知對話的流程


## 思考邏輯  

`main.py`  
1. 在旅客使用此專案是會依照`prompts.py/TRAVEL_PROMPT`詢問說"本次旅遊要前往的地點"   
2. 將旅客的需求透過`prompts.py/FORMAT_SETTING_PROMPT`轉換`list`格式並做成Tasks  
 
`run.py`  
3. 將Tasks透過WebVoyager進行網頁搜索  

`main.py`   
4. 輸出至前端讓顧客明瞭目前的執行進度以及思考內容    
5. 回到第三步直至Tasks完成  
6. 將所有的Tasks的內容儲存並且透過`prompts.py/TRAVEL_END_PROMPT`進行本次旅遊體驗的總結  
7. 回到第一步直至結束  

   

### 執行結果

經測試後可以更新`main.py`的記憶  
#### main.py 
1.   第一次嘗試  
輸入 I want to go to taipei  
在`result/20250414_13_36_50/1/interact_messages.json`可以查看travel-agent完整的對話流程  
結果為以下 

tasks number: 3

Dear Traveler,

Your upcoming trip to Taipei on April 17th is shaping up to be a delightful experience. Here's a comprehensive travel plan to ensure you make the most of your visit:

**Accommodation**:
You’re all set to find a cozy hotel in Taipei for two guests, with a budget cap of NT$5000 for your one-night stay on April 17th. Rest assured that we are searching for the best deals to match your needs.

**Weather Forecast**:
Expect a pleasant day in Taipei on April 17th, with sunny skies. Daytime temperatures will range from a comfortable 19°C to a warm 30°C, while the nighttime temperatures will cool down to between 21°C and 25°C. Dressing in light, breathable clothing and packing a light jacket for the evening would be ideal.

**Must-Visit Attractions**:
Make sure to explore some of Taipei's cultural and historical gems. Highlights include the imposing National Chiang Kai-shek Memorial Hall, the famed National Palace Museum with its vast collection of art, and the beautiful and spiritually enriching Lungshan Temple. Each location offers a unique glimpse into Taipei's rich heritage.

Feel free to reach out if you need further assistance or have specific preferences for your accommodations or sightseeing plans. Our mission is to ensure you have a seamless and memorable experience in Taipei.

Safe travels and enjoy your adventure!

Warm regards,

[Your Name]
Professional Travel Assistant

**可以發現對於飯店查詢無法成功提供資訊**  

---

2. 第二次嘗試  
輸入 sure, please find a hotel   
在`result/20250414_13_36_50/2/interact_messages.json`可以查看travel-agent完整的對話流程  
結果為以下  
   
tasks number: 1

最後總結   
Certainly! Here is your comprehensive travel plan to Taipei:

**Accommodation:**
You will be staying at the elegant Caesar Park Hotel (台北凱達大飯店) in Taipei. This hotel meets your budget perfectly, costing just $3,183 per night. It offers comfort and convenience, located in an ideal area to explore the city.

**Weather Forecast:**
On your check-in date, April 17th, Taipei will delight you with sunny weather during the day, with temperatures ranging from a pleasant 19°C to 30°C. The night will cool down slightly to 21°C to 25°C, perfect for an evening stroll or a quiet dinner.

**Tourist Attractions:**
While in Taipei, you have a range of exciting places to visit:
1. **National Chiang Kai-shek Memorial Hall** - Immerse yourself in the history and culture of Taiwan.
2. **National Palace Museum** - Discover an extensive collection of priceless Chinese art and artifacts.
3. **Lungshan Temple** - Experience the tranquil beauty of this historic Buddhist temple.

With everything perfectly set up for your trip, all that remains is for you to enjoy your journey to Taipei. Should you need any more assistance, feel free to reach out. Have a wonderful trip!

**此次結果有出現飯店資訊**  

---

3. 第三次嘗試  
嘗試修改地點，輸入 maybe we can go to taoyuan  
在`result/20250414_13_36_50/3/interact_messages.json`可以查看travel-agent完整的對話流程  
結果為以下  
   
tasks number: 3


---
#### run.py (WebVoyager) 
Here's a tailored travel plan for your delightful upcoming trip to Taoyuan:

**Accommodation:**
I've found an ideal hotel for your stay in Taoyuan, suited for 2 guests, checking in on April 17th for one night within the budget of NT$5000. Please let me know if you need more options or detailed listing and booking assistance.

**Weather Forecast:**
On April 17th, Taoyuan will greet you with pleasant sunny weather during the day with temperatures ranging between 22°C and 28°C. As evening sets in, expect a partly cloudy sky and temperatures between 18°C and 26°C, perfect for evening strolls or night markets explorations.

**Must-Visit Attractions:**
While you're in Taoyuan, you should consider visiting these top attractions:
1. **虎頭山公園 (Hutoushan Park):** A serene park perfect for a relaxing walk or peaceful picnic amidst nature.
2. **大溪老街 (Daxi Old Street):** Discover the charming historical architecture and delightful local treats on this bustling street.
3. **中壢區觀光夜市 (Zhongli Night Market):** Dive into the vibrant Taiwanese night market culture with delicious street food and exciting shopping.
4. **台茂購物中心 (TaiMall Shopping Center):** A haven for shopping enthusiasts with a great variety of stores and entertainment options.

Feel free to reach out if you have any more preferences or need further assistance. Enjoy your trip to Taoyuan, filled with beautiful sights and cultural experiences! Safe travels!

在找尋飯店上WebVoyager會**一直卡住在桃園國際機場**，而無法前往下一步資訊。