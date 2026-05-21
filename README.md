# MHNow Info Hub — セットアップ・編集ガイド

## ブラウザで開く（ローカル確認）

`index.html` をダブルクリックするだけで Chrome / Edge などで開けます。

---

## スマホ・PC どこからでも見れるようにする（GitHub Pages）

### 1. GitHub アカウントを作る
https://github.com にアクセスして無料アカウントを作成。

### 2. 新しいリポジトリを作る
- 右上の「＋」→「New repository」
- Repository name: `mhnow-info`（任意）
- Public を選択
- 「Create repository」をクリック

### 3. ファイルをアップロード
- 「uploading an existing file」リンクをクリック
- `index.html` と `data.js` を両方ドラッグ＆ドロップ
- 「Commit changes」をクリック

### 4. GitHub Pages を有効にする
- リポジトリの「Settings」タブ
- 左メニュー「Pages」
- Branch: `main` / フォルダ: `/ (root)` を選択して「Save」
- 数分後、`https://あなたのID.github.io/mhnow-info/` で公開完了！

---

## コンテンツの更新方法

**`data.js` だけ編集すれば OK です。**  
GitHub 上でもウェブブラウザから直接編集できます。

### GitHub 上で編集する手順
1. リポジトリの `data.js` をクリック
2. 右上の鉛筆アイコン（Edit）をクリック
3. 内容を書き換える
4. 「Commit changes」で保存 → 即サイトに反映

---

## 各セクションの編集例

### 公式情報を追加する

`data.js` の `official: [` の中に以下をコピーして追加：

```js
{
  id: 5,                         // ← 連番で増やす
  date: "2026-05-25",            // ← 日付
  category: "イベント",           // ← アップデート / イベント / お知らせ / メンテナンス
  title: "ここにタイトル",
  summary: "ここに概要文",
  url: "https://www.monsterhunternow.com/ja-JP/news",
  isNew: true                    // ← 新着表示する場合 true
},
```

### SNS装備を追加する

`data.js` の `sns: [` の中に追加。  
YouTube動画を埋め込む場合は `youtubeId` に動画IDを入力：

```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
                                ↑ここがID
```

```js
youtubeId: "dQw4w9WgXcQ",  // ← この部分だけコピー
```

### 大量発生イベントを追加する

`data.js` の `outbreak: [` の中に追加。  
`isActive: true` で「開催中」バッジが付きます。

### 拠点要撃戦の情報を更新する

`defense:` の中の `current:` 部分を書き換えるだけです。

---

## よくある質問

**Q. スマホで編集できる？**  
A. GitHub のモバイルアプリ（GitHub Mobile）からも編集できます。

**Q. 複数人で管理したい**  
A. GitHub の「Collaborators」設定で他の人を招待できます。

**Q. 更新が反映されない**  
A. ブラウザのキャッシュをクリアしてみてください（Ctrl+Shift+R）。
