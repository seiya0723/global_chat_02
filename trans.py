from googletrans import Translator
translator = Translator()


string_ja = "今日も頑張ってPythonを勉強しよう。"
# string_ja = "Djangoの勉強は楽しいなあ！君もそう思うよね！Djangoでウェブアプリ作るのが楽しい！ああああ"

#src引数は無くても良い
# trans_en = translator.translate(string_ja, src="en", dest="ja")
# print(trans_en.text)

# trans_en = translator.translate(string_ja, src="ja", dest="en")
# print(trans_en.text)

# trans_en = translator.translate(string_ja, src="ja", dest="ja")
# print(trans_en.text)
# trans_en = translator.translate(string_ja, src="ja", dest="ko")
# print(trans_en.text)
# trans_en = translator.translate(string_ja, src="ja", dest="ko")
# print(trans_en.text)
# trans_en = translator.translate(string_ja, src="ja", dest="ko")
# print(trans_en.text)
# trans_en = translator.translate(string_ja, src="ja", dest="ko")
# print(trans_en.text)


trans_en = translator.translate(string_ja, dest="ja")
print(trans_en.text)
trans_en = translator.translate(string_ja, dest="en")
print(trans_en.text)
trans_en = translator.translate(string_ja, dest="zh-CN")
print(trans_en.text)
trans_en = translator.translate(string_ja, dest="ko")
print(trans_en.text)
trans_en = translator.translate(string_ja, dest="de")
print(trans_en.text)
trans_en = translator.translate(string_ja, dest="fr")
print(trans_en.text)