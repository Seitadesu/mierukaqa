from janome.tokenizer import Tokenizer
from PIL import Image, ImageDraw, ImageFont
from wordcloud import WordCloud

def create_cloud(word_q_answer, page_id):
    tk = Tokenizer()
    words = []
    for q_answer in word_q_answer:
        line_words = []
        prev_token = None
        for token in tk.tokenize(q_answer[0]):
            pos = token.part_of_speech.split(",")[0]
            if pos in ["名詞","動詞","形容詞","副詞","代名詞","固有名詞","感動詞"]:
                if prev_token and prev_token.part_of_speech.split(",")[0] in ["名詞"]:
                    line_words[-1] = line_words[-1]+token.surface
                elif prev_token and prev_token.part_of_speech.split(",")[0] in ["助動詞"]:
                    if prev_token.surface in ["ない", "なかっ", "ませ"]:
                        line_words.append(token.surface+prev_token.surface)
                    else:
                        line_words.append(token.base_form)
                else:
                    line_words.append(token.base_form)
            prev_token = token
        line_words = [word for word in line_words if word!='']
        words.extend(line_words)
    words = " ".join(words)






    # ワードクラウドを作成
    wordcloud = WordCloud(background_color="white", stopwords={"もの","これ","ため","それ","ところ","よう","の","です","だ","は","が","思う","思い","感じた","感じる"
    }, collocations = False, font_path="./static/fonts/YuGothM.ttc", width=600, height=400, max_words=50, include_numbers=True).generate(words)


    #ワードクラウド画像を保存する
    wordcloud.to_file("./static/image/wordcloud"+str(page_id)+".png")

    #ワードクラウド画像を読み込む
    wordcloud_img = Image.open("./static/image/wordcloud"+str(page_id)+".png")


    #ロゴ画像を読み込む
    logo_img = Image.open("./static/image/logonosukashi.png")

    #ワードクラウド画像の上にロゴ画像を重ねる
    wordcloud_img.paste(logo_img, (wordcloud_img.width - logo_img.width, 0), logo_img)

    #合成した画像を保存する
    wordcloud_img.save("./static/image/wordcloud"+str(page_id)+".png")
