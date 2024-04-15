# Set working directory
getwd()
setwd("./../Desktop/mybaby")

# Load libraries
library(readtext)
library(quanteda)
library(jiebaR)
library(stopwords)
library(stringr)
library(readxl)
library(tidytext)
library(tidyverse)
library(rvest)
library(dplyr)
library(magrittr)
library(knitr)
library(tmcn)
library(wordcloud2) 
library(wordcloud)


# Read data
data <- read_excel("data.xlsx")
text_column_index <- which(colnames(data) == "Comment")
text <- as.character(data[, text_column_index])
head(data)

# Remove URLs
text <- str_replace_all(text, "https?://\\S+", "")


# Special words
special_words <- c("エマ", "でびる", "葛葉", "XD", "XDD", "XDDD", "XDDDD", 
                   "XDDDDD", "柴卡", "裸卡", "くん", "伊甸組", "w", "ww", "www", "笑死", "るる", 
                   "SEEDs", "486", "LOL", "尊媽", "twitch", "ban", "あかりん", "C4", "LUCA", "千草"
                   , "Apex", "apex", "すみれ", "のあ")


# Tokenization with custom words


seg <- worker(bylines = FALSE)
for (i in 1:length(special_words)) {
  new_user_word(seg, special_words[i])
}

segment_result <- segment(text, seg)

# Load  stopwords
stopwords_TW <- read_table("stopwords.txt", col_names = FALSE)$X1

# Remove stopwords
segment_result <- segment_result[!segment_result %in% stopwords_TW]


# Display results
head(segment_result, 50)



#######################
# count num of article
#######################
article_counts <- data %>%
  group_by(Type) %>%
  summarise(total_articles = n())
 
article_counts 

#######################
# count average like
#######################
average_likes <- data %>%
  group_by(Type) %>%
  summarise(average_likes = mean(Like))

average_likes

#######################
# count average comment num
#######################
average_comment <- data %>%
  group_by(Type) %>%
  summarise(total_comment_num = mean(CommentNum))

average_comment

################################
##comment
#################################

data$Time <- as.POSIXct(data$Time)

# 依序撈出三種 Type 的 Comment
Holo_comments <- data %>%
  filter(Type == "H") %>%
  select(Comment)

Niji_comments <- data %>%
  filter(Type == "N") %>%
  select(Comment)

X_comments <- data %>%
  filter(Type == "X") %>%
  select(Comment)

# remove URLs
Holo_comments$Comment <- str_replace_all(Holo_comments$Comment, "https?://\\S+", "")
Niji_comments$Comment <- str_replace_all(Niji_comments$Comment, "https?://\\S+", "")
X_comments$Comment <- str_replace_all(X_comments$Comment, "https?://\\S+", "")


# 斷詞

Holo_words <- segment(Holo_comments$Comment, seg)
Niji_words <- segment(Niji_comments$Comment, seg)
X_words <- segment(X_comments$Comment, seg)

# 加入停用詞
Holo_words <- Holo_words[!Holo_words %in% stopwords_TW]
Niji_words <- Niji_words[!Niji_words %in% stopwords_TW]
X_words <- X_words[!X_words %in% stopwords_TW]


# 計算詞頻
Holo_word_freq <- freq(Holo_words)
Niji_word_freq <- freq(Niji_words)
X_word_freq <- freq(X_words)

# 取得 Top 20 詞
top20_Holo <- head(Holo_word_freq[order(Holo_word_freq$freq, decreasing = TRUE), ], 20)
top20_Niji <- head(Niji_word_freq[order(Niji_word_freq$freq, decreasing = TRUE), ], 20)
top20_X <- head(X_word_freq[order(X_word_freq$freq, decreasing = TRUE), ], 20)

top20_Holo


# 繪製詞頻長條圖

barplot(top20_Holo$freq, main = "Top 20 Words in Hololive", col = "lightblue", las = 2, names.arg = top20_Holo$char)


barplot(top20_Niji$freq, main = "Top 20 Words in Nijisanji", col = "lightgreen", las = 2, names.arg = top20_Niji$char)


barplot(top20_X$freq, main = "Top 20 Words in Other Type", col = "lightcoral", las = 2, names.arg = top20_X$char)



#################################
# wordcloud
################


# 調整顏色方案
library(RColorBrewer)
colors <- brewer.pal(8, "Dark2")
any(Holo_word_freq$freq == 0)
# 繪製 Hololive 文字雲
par(family=("Microsoft YaHei"))
set.seed(1234)
wordcloud(Holo_word_freq$char, Holo_word_freq$freq, min.freq = 20, random.order = F, ordered.colors = F, colors = rainbow(nrow(Holo_word_freq)))




#############
 # for reproducibility 

wordcloud2(filter(Holo_freq, freq > 10), 
           minSize = 2, fontFamily = "Microsoft YaHei", size = 0.75, color='random-light', backgroundColor="black")




wordcloud2(filter(Niji_freq, freq > 500), 
           minSize = 2, fontFamily = "Microsoft YaHei", size = 0.73, color='random-light', backgroundColor="black")

#X_freq <- freq(X_words)
wordcloud2(filter(X_freq, freq > 250), 
           minSize = 2, fontFamily = "Microsoft YaHei", size = 0.55, color='random-light', backgroundColor="black")

########################################
# Time
#############################

Holo_articles <- data %>%
  filter(Type == "H")

Niji_articles <- data %>%
  filter(Type == "N")

X_articles <- data %>%
  filter(Type == "X")

# 計算每日文章數量
Holo_daily_counts <- table(format(Holo_articles$Time, "%Y-%m-%d"))
Niji_daily_counts <- table(format(Niji_articles$Time, "%Y-%m-%d"))
X_daily_counts <- table(format(X_articles$Time, "%Y-%m-%d"))

# each graph


# 合併三個 Type 的文章數據
combined_counts <- rbind(
  data.frame(Time = as.Date(names(Holo_daily_counts)), Count = as.numeric(Holo_daily_counts), Type = "Hololive"),
  data.frame(Time = as.Date(names(Niji_daily_counts)), Count = as.numeric(Niji_daily_counts), Type = "Nijisanji"),
 data.frame(Time = as.Date(names(X_daily_counts)), Count = as.numeric(X_daily_counts), Type = "X")
)

holo_article_freq <- data.frame(Time = as.Date(names(Holo_daily_counts)), Count = as.numeric(Holo_daily_counts), Type = "H")
niji_article_freq <- data.frame(Time = as.Date(names(Niji_daily_counts)), Count = as.numeric(Niji_daily_counts), Type = "N")
x_article_freq <- data.frame(Time = as.Date(names(X_daily_counts)), Count = as.numeric(X_daily_counts), Type = "X")



# 假設你有三個 data.frame: holo_article_freq, niji_article_freq, x_article_freq

ggplot(holo_article_freq, aes(x = Time, y = Count)) +
  geom_line(color = "lightblue") +
  labs(title = "Daily Article Counts", y = "", x="") +
  theme_minimal() +
  facet_grid(Type ~ ., scales = "free_y") +
  guides(color = FALSE) +
  theme(strip.text = element_blank()) 


ggplot(niji_article_freq, aes(x = Time, y = Count)) +
  geom_line(color = "lightgreen") +
  labs(title = "Daily Article Counts", y = "", x="") +
  theme_minimal() +
  facet_grid(Type ~ ., scales = "free_y") +
  guides(color = FALSE) +
  theme(strip.text = element_blank()) +
  scale_color_manual(values = "lightgreen")

ggplot(x_article_freq, aes(x = Time, y = Count)) +
  geom_line(color = "lightcoral") +
  labs(title = "Daily Article Counts", y = "", x="") +
  theme_minimal() +
  facet_grid(Type ~ ., scales = "free_y") +
  guides(color = FALSE) +
  theme(strip.text = element_blank()) +
  scale_color_manual(values = "lightgreen")


# 轉換 Time 到日期格式
combined_counts$Time <- as.Date(combined_counts$Time)

# 繪製摺線圖
ggplot(combined_counts, aes(x = Time, y = Count, color = Type)) +
  geom_line() +
  labs(title = "Daily Article Counts by Type", x = "Time", y = "Article Counts") +
  theme_minimal()+
  facet_grid(Type ~ ., scales = "free_y")



X_counts <- data.frame(Time = as.Date(names(X_daily_counts)), Count = as.numeric(X_daily_counts), Type = "X")
X_counts$Time <- as.Date(X_counts$Time)
ggplot(X_counts, aes(x = Time, y = Count, color = Type)) +
  geom_line() +
  labs(title = "Daily Article Counts by Type", x = "Time", y = "Article Counts") +
  theme_minimal()

###############################################
# 合併 Hololive 和 Nijisanji 的文章數據
holo_niji_counts <- rbind(
  data.frame(Time = as.Date(names(Holo_daily_counts)), Count = as.numeric(Holo_daily_counts), Type = "Hololive"),
  data.frame(Time = as.Date(names(Niji_daily_counts)), Count = as.numeric(Niji_daily_counts), Type = "Nijisanji")
)

# 轉換 Time 到日期格式
holo_niji_counts$Time <- as.Date(holo_niji_counts$Time)

# 繪製彩色長條圖
ggplot(holo_niji_counts, aes(x = Time, y = Count, fill = Type)) +
  geom_col(position = "stack") +
  labs(title = "Daily Article Counts by Type", x = "Time", y = "Article Counts") +
  scale_fill_manual(values = c("Hololive" = "lightblue", "Nijisanji" = "lightgreen")) +
  theme_minimal()


