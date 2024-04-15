import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import re


# 函數用來取得每一頁的資料
def get_page_data(url):
    response = requests.get(url, headers={'cookie': 'over18=1;'})
    response.encoding = 'utf-8'  # 指定正確的編碼
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.select("div.title")
    page_data = []

    for item in results:
        title = item.text.strip()

        # classification
        # 判斷是否包含 hololive 關鍵字
        is_hololive_related = any(keyword in title for keyword in hololive_keywords)
        # 判斷是否包含 にじさんじ 或 彩虹社 關鍵字
        is_nijisanji_related = any(keyword in title for keyword in nijisanji_keywords)

        # 根據判斷結果進行分類並存入列表
        if is_hololive_related:
            classification = "H"
        elif is_nijisanji_related:
            classification = "N"
        else:
            classification = "X"

        # scrap comment
        a_tag = item.select_one("a")
        if a_tag:
            href = a_tag.get("href")
            href = "https://www.ptt.cc" + href

            # catch comment
            response = requests.get(href)
            soup = BeautifulSoup(response.text, 'lxml')
            articles = soup.find_all('div', 'push')
            each_comment = []
            for article in articles:
                #messages = article.find('span', 'f3 push-content').getText()
                push_content_span = article.find('span', 'f3 push-content')
                # 如果找不到 'span' 標籤和 'f3 push-content' class，將 messages 設為空字符串
                messages = push_content_span.getText() if push_content_span else ""
                #print(messages)
                each_comment.append(messages)

            # catch time
            time_elements = soup.select('span.article-meta-value')
            #print(time_elements)
            if len(time_elements) > 3:
                #print(time_elements[3].text)
                post_time = time_elements[3].text
                if len(post_time.split()) == 4:
                    post_time = ' '.join([post_time.split()[0], post_time.split()[1], '12', '00:00:00', post_time.split()[3]])
                    print(post_time)
                post_datetime = datetime.strptime(post_time, '%a %b %d %H:%M:%S %Y')
            elif len(time_elements) == 3:
                print(time_elements[2].text)
                post_time = time_elements[2].text
            else:
                # 如果找不到時間元素，為 post_datetime 賦一個預設值（當前的系統時間）
                post_datetime = ""


            # catch push
            like = dislike = other = 0
            for i in soup.find_all('div', 'push'):
                temp = i.find('span')
                if temp is None:
                    break
                else:
                    if temp.getText() == '推 ':
                        like += 1
                    elif temp.getText() == '噓 ':
                        dislike += 1
                    else:
                        other += 1
            total = like + dislike + other

            page_data.append({'Title': title, 'Type': classification, 'Time': post_datetime,
                              'Like': like, 'Dislike': dislike,
                              'CommentNum': total, 'Comment': each_comment})

    return page_data


# 關鍵字列表
hololive_keywords = ["hololive", "ホロライブ", "スバル","holo","時乃空",
    "ときのそら",
    "蘿蔔子",
    "ロボ子さん",
    "星街彗星",
    "星街すいせい",
    "櫻巫女",
    "さくらみこ",
    "AZKi",
    "あずき",
    "夜空梅露",
    "夜空メル",
    "白上吹雪",
    "白上フブキ",
    "亞綺·羅森塔爾",
    "アキ・ローゼンタール",
    "夏色祭",
    "夏色まつり",
    "赤井心",
    "赤井はあと",
    "湊阿庫婭",
    "湊あくあ",
    "紫咲詩音",
    "紫咲シオン",
    "百鬼綾目",
    "百鬼あやめ",
    "癒月巧可",
    "癒月ちょこ",
    "大空昴",
    "大空スバル",
    "白上吹雪",
    "大神澪",
    "大神ミオ",
    "貓又小粥",
    "猫又おかゆ",
    "戌神沁音",
    "戌神ころね",
    "兔田佩克拉",
    "兎田ぺこら",
    "船長",
    "不知火芙蕾雅",
    "不知火フレア",
    "白銀諾艾爾",
    "白銀ノエル",
    "寶鐘瑪琳",
    "宝鐘マリン",
    "天音彼方",
    "天音かなた",
    "角卷綿芽",
    "角巻わため",
    "常闇永遠",
    "常闇トワ",
    "姬森璐娜",
    "姫森ルーナ",
    "雪花菈米",
    "雪花ラミィ",
    "桃鈴音音",
    "桃鈴ねね",
    "獅白牡丹",
    "獅白ぼたん",
    "尾丸波爾卡",
    "尾丸ポルカ",
    "拉普拉斯·達克尼斯",
    "ラプラス・ダークネス",
    "鷹嶺琉依",
    "鷹嶺ルイ",
    "博衣小夜璃",
    "博衣こより",
    "沙花叉克蘿耶",
    "沙花叉クロヱ",
    "風真伊呂波",
    "風真いろは",
    "友人A",
    "春先和花",
    "春先のどか", 
    "潤羽露西婭",
    "潤羽るしあ",
"桐生可可", 
"桐生ココ", "森美聲", "森カリオペ", "Mori Calliope", "小鳥遊琪亞拉", "小鳥遊キアラ", "Takanashi Kiara", "一伊那爾栖", "Ninomae Ina'nis", 
"古拉", "Gura", 
"華生", "ワトソン・アメリア", "IRyS"
]

nijisanji_keywords = ["にじさんじ", "彩虹社","葛葉", "笹木咲", "kuzuha", "Kuzuha", "Kanae",
    "月之美兔", "月ノ美兎",
    "樋口楓",
    "靜凜",
    "勇氣千尋", "勇気ちひろ",
    "艾露", "える",
    "鈴谷秋", "鈴谷アキ",
    "摩伊拉", "モイラ",
    "澀谷初", "渋谷ハジメ",
    "鈴鹿詩子",
    "宇志海莓", "宇志海いちご",
    "家長麥", "家長むぎ",
    "夕陽莉莉", "夕陽リリ",
    "伏見學", "伏見ガク",
    "吉爾扎倫三世", "ギルザレンIII世",
    "劍持刀也", "剣持刀也",
    "物述有栖",
    "文野環",
    "森中花咲",
    "叶", "かなえ",
    "赤羽葉子",
    "笹木咲",
    "本間向日葵", "本間ひまわり",
    "魔界之莉莉姆", "魔界ノりりむ",
    "葛葉",
    "椎名唯華",
    "多拉", "ドーラ",
    "轟京子",
    "修女·克蕾雅", "シスター・クレア",
    "花畑嘉依卡", "花畑チャイカ",
    "社築",
    "安土桃",
    "卯月光", "卯月コウ",
    "鈴木勝",
    "綠仙",
    "神田笑一",
    "飛鳥雛", "飛鳥ひな",
    "春崎艾爾", "春崎エアル",
    "雨森小夜",
    "鷹宮莉音", "鷹宮リオン",
    "舞元啟介",
    "舞元",
    "龍膽尊", "竜胆尊",
    "德比德比·德比魯", "でびでび・でびる",
    "櫻凜月",
    "町田千麻", "町田ちま",
    "周·力一", "ジョー・力一",
    "成瀨鳴",
    "貝爾蒙德·班德拉斯", "ベルモンド・バンデラス",
    "矢車理音", "矢車りね",
    "夢追翔",
    "黑井柴", "黒井しば",
    "郡道美玲",
    "夢月蘿婭", "夢月ロア",
    "小野町春香",
    "語部紡",
    "瀨戶美夜子",
    "戌亥床", "戌亥とこ",
    "安潔·卡特莉娜", "アンジュ・カトリーナ",
    "莉澤·赫露艾斯塔", "リゼ・ヘルエスタ",
    "三枝明那",
    "愛園愛美",
    "雪城真尋",
    "エクス・アルビオ",
    "利維·艾莉法", "レヴィ・エリファ",
    "葉山舞鈴",
    "紐伊·索西艾瑞", "ニュイ・ソシエール",
    "葉加瀨冬雪",
    "加賀美隼人", "加賀美ハヤト",
    "夜見蕾娜", "夜見れな",
    "阿露絲·阿爾瑪", "アルス・アルマル",
    "相羽初葉", "相羽ういは",
    "天宮心", "天宮こころ",
    "艾莉·柯妮法", "エリー・コニファー",
    "拉特娜·葡蒂", "ラトナ・プティ",
    "早瀨走",
    "健屋花那",
    "謝林·伯艮第", "シェリン・バーガンディ",
    "星川莎拉", "星川サラ",
    "文美", "フミ",
    "山神歌流多", "山神カルタ",
    "艾瑪★奧加斯特", "えま★おうがすと",
    "魔使真央", "魔使マオ",
    "路易斯·嘉米", "ルイス・キャミー",
    "不破湊",
    "白雪巴",
    "圭利·奧什·迦爾", "グウェル・オス・ガール",
    "真白爻", "ましろ爻",
    "奈羅花",
    "來栖夏芽",
    "組合名 - 冥府", "メイフ",
    "芙蓮·E·露絲塔莉歐", "フレン・E・ルスタリオ",
    "伊卜拉新", "イブラヒム",
    "弦月藤士郎",
    "甲斐田晴",
    "長尾景",
    "空星煌", "空星きらめ",
    "周央珊瑚", "周央サンゴ",
    "東堂琥珀", "東堂コハク",
    "北小路翡翠", "北小路ヒスイ",
    "西園千草", "西園チグサ",
    "ローレン・イロアス",
    "レオス・ヴィンセント",
    "オリバー・エバンス",
    "レイン・パターソン",
    "海妹四葉",
    "天瀨夢癒",
    "天ヶ瀬むゆ",
    "先斗寧",
    "壹百滿天原莎樂美",
    "莎樂美",
    "壱百満天原サロメ"
]

# 設定起始頁面和總頁數
start_url = "https://www.ptt.cc/bbs/Vtuber/index.html"
total_pages = 732
#total_pages = 3
prev_post_datetime = 0

# 爬取多頁面的資料
all_data = []
for page in range(total_pages):
    page_data = get_page_data(start_url)
    all_data.extend(page_data)
   # 找到上一頁的 a 標籤
    prev_page_link = BeautifulSoup(requests.get(start_url).text, 'html.parser').find('a', class_='btn wide', string='‹ 上頁')

    
    if prev_page_link:
        # 使用正規表達式找到 href 中的數字部分，並將其減一
        page_number = re.search(r'\d+', prev_page_link['href']).group()
        start_url = f"https://www.ptt.cc/bbs/Vtuber/index{int(page_number)}.html"
        print(start_url)
    else:
        print("Its the first one cannot get another one")
        break

# 將資料存入 DataFrame
df = pd.DataFrame(all_data)

# 將 DataFrame 寫入 Excel 文件
df.to_excel('data.xlsx', index=False)
