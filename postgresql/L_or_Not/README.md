# 中間テーブルの有無を比較する

タグを情報を付与する場合に、中間テーブルを用いるべきかどうかを実際にテスト環境で試してみる

## 検証条件

企業数：300万
タグ数：1万
1つのタグは50~2万の範囲で会社に紐づきます。

平均タグ数：平均14個(標準偏差5)

テーブル形式

companies
・id
・name

all_in_tag
・id
・company_id
・tag_name

l_company_tag
・id
・company_id
・tag_id

tags
・id
・tag
