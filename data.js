// ================================================================
//  data.js — MHNow Info Hub コンテンツ管理ファイル
// ================================================================
//  ★ このファイルを編集してアプリの内容を更新します ★
//
//  【編集の基本ルール】
//  ・文字列は " " （ダブルクォート）で囲む
//  ・日付は "YYYY-MM-DD" 形式（例: "2026-05-21"）
//  ・true = はい、false = いいえ
//  ・カンマ , の位置を変えないよう注意！
// ================================================================

const MH_DATA = {

  // 最終更新日（ヘッダーに表示）
  lastUpdated: "2026-05-21",

  // ==============================================================
  //  公式情報セクション
  //  カテゴリ: "アップデート" / "イベント" / "お知らせ" / "メンテナンス"
  // ==============================================================
  official: [
    {
      id: 1,
      date: "2026-05-20",
      category: "イベント",
      title: "大量発生ウィーク：砂漠の王者",
      summary: "ジュラトドス・バギィなど砂漠系モンスターが大量発生。限定素材でレア武器が作成可能。期間中はフィールド密度2倍。",
      url: "https://www.monsterhunternow.com/ja-JP/news",
      isNew: true
    },
    {
      id: 2,
      date: "2026-05-15",
      category: "アップデート",
      title: "Ver.78.1：操虫棍・猟虫育成システム追加",
      summary: "操虫棍が正式実装。猟虫は素材で強化でき、属性・スタミナ回復などの恩恵を付与可能。既存武器のバランス調整あり（双剣の連続攻撃強化）。",
      url: "https://www.monsterhunternow.com/ja-JP/news",
      isNew: false
    },
    {
      id: 3,
      date: "2026-05-10",
      category: "お知らせ",
      title: "拠点要撃戦シーズン2 開幕・報酬刷新",
      summary: "シーズン2スタート。X素材の入手率UP、シーズンランキング報酬にレア装飾品追加。シーズン1の未消費ポイントは自動変換。",
      url: "https://www.monsterhunternow.com/ja-JP/news",
      isNew: false
    },
    {
      id: 4,
      date: "2026-05-05",
      category: "メンテナンス",
      title: "5/5 メンテナンス完了（約2時間）",
      summary: "不具合修正・サーバー安定化のためのメンテナンス。一部クエスト報酬の二重取得バグを修正。",
      url: "https://www.monsterhunternow.com/ja-JP/news",
      isNew: false
    }
  ],

  // ==============================================================
  //  SNS装備紹介セクション
  //  source: "YouTube" / "X" / "その他"
  //  youtubeId: YouTube動画IDを入力すると埋め込み表示
  //             （例 https://youtu.be/dQw4w9WgXcQ → "dQw4w9WgXcQ"）
  //  difficulty: "初心者向け" / "中級者向け" / "上級者向け"
  // ==============================================================
  sns: [
    {
      id: 1,
      title: "【操虫棍】全属性対応！汎用ビルド完全解説",
      source: "YouTube",
      author: "MHNow攻略チャンネル",
      url: "https://www.youtube.com/watch?v=example1",
      youtubeId: "",
      weapon: "操虫棍",
      weaponElement: "なし",
      difficulty: "中級者向け",
      armorSkills: ["弱点特攻Lv3", "属性攻撃強化Lv5", "連撃Lv3", "体力増強Lv3"],
      tags: ["汎用", "属性対応"],
      notes: "猟虫は蒼赤系がおすすめ。属性武器を複数用意して持ち替えると属性ダメージがさらにUP。猟虫バフを常に維持することが火力の鍵。"
    },
    {
      id: 2,
      title: "【大剣】リオレウス特化 溜め斬り最大火力ビルド",
      source: "X",
      author: "@MHNow_DaikenPro",
      url: "https://x.com/example",
      youtubeId: "",
      weapon: "大剣",
      weaponElement: "水",
      difficulty: "上級者向け",
      armorSkills: ["集中Lv3", "弱点特攻Lv3", "超会心Lv3", "耐熱Lv2"],
      tags: ["高火力", "リオレウス対策"],
      notes: "真溜め斬りのタイミングが命。飛び上がり直後の着地に合わせて溜めを開始すると安定してヒットする。尻尾部位狙いで素材効率UP。"
    },
    {
      id: 3,
      title: "【ランス】初心者でも死なない！防御特化ビルド",
      source: "YouTube",
      author: "らくらくハンター",
      url: "https://www.youtube.com/watch?v=example2",
      youtubeId: "",
      weapon: "ランス",
      weaponElement: "なし",
      difficulty: "初心者向け",
      armorSkills: ["ガード強化Lv3", "体力増強Lv3", "不屈Lv1", "スタミナ急速回復Lv2"],
      tags: ["初心者向け", "安全重視", "拠点要撃向け"],
      notes: "ガード性能を最大まで積むと大半の攻撃をガードできる。回復薬との併用で長期戦を安定してこなせる。拠点要撃戦のサポート役にも最適。"
    },
    {
      id: 4,
      title: "【双剣】属性4本持ち！汎用最速狩りビルド",
      source: "X",
      author: "@SousouMaster_MHN",
      url: "https://x.com/example2",
      youtubeId: "",
      weapon: "双剣",
      weaponElement: "火・水・雷・氷",
      difficulty: "中級者向け",
      armorSkills: ["属性攻撃強化Lv5", "回避性能Lv3", "スタミナ急速回復Lv3", "体力増強Lv2"],
      tags: ["速攻", "大量発生向け", "汎用"],
      notes: "属性4本持ちが基本。鬼人化中は鬼人強化が乗るのでスタミナ管理が重要。大量発生時の周回速度は全武器でもトップクラス。"
    }
  ],

  // ==============================================================
  //  大量発生イベントセクション
  //  element: "火" / "水" / "雷" / "氷" / "龍" / "なし"
  //  weaknesses: 0=なし 1=弱点(★) 2=特効(★★)
  //  isActive: true=開催中, false=近日開催
  // ==============================================================
  outbreak: [
    {
      id: 1,
      monster: "リオレウス",
      icon: "🦅",
      startDate: "2026-05-20",
      endDate: "2026-05-27",
      isActive: true,
      starRating: 5,
      element: "火",
      weaknesses: {
        fire:    0,
        water:   2,
        thunder: 1,
        ice:     2,
        dragon:  1
      },
      recommendedElement: "水・氷",
      keySkills: ["耐熱Lv2以上", "体力増強Lv3", "弱点特攻Lv3"],
      tips: "空中に逃げたら追わずに回避に専念。尻尾を切断すると毒攻撃が消えて難易度が下がる。飛びかかりの予備動作（低空ホバリング）を見たら即回避。",
      mainRewards: ["リオレウスの翼爪", "ヘビィーコート"],
      rareRewards: ["竜玉"]
    },
    {
      id: 2,
      monster: "ジュラトドス",
      icon: "🐊",
      startDate: "2026-05-15",
      endDate: "2026-05-28",
      isActive: true,
      starRating: 4,
      element: "水",
      weaknesses: {
        fire:    2,
        water:   0,
        thunder: 1,
        ice:     0,
        dragon:  0
      },
      recommendedElement: "火",
      keySkills: ["耐水Lv2", "回避性能Lv3", "弱点特攻Lv3"],
      tips: "砂地エリアでは突進速度が増す。水ブレスは横転で回避。頭部への攻撃がひるみを取りやすく、スタンを狙いやすい。",
      mainRewards: ["ジュラトドスの鱗", "水袋"],
      rareRewards: ["竜骨【大】"]
    },
    {
      id: 3,
      monster: "ベリオロス",
      icon: "🐉",
      startDate: "2026-05-22",
      endDate: "2026-05-29",
      isActive: false,
      starRating: 5,
      element: "氷",
      weaknesses: {
        fire:    2,
        water:   0,
        thunder: 1,
        ice:     0,
        dragon:  1
      },
      recommendedElement: "火",
      keySkills: ["耐寒Lv2以上", "回避距離UPLv3", "体力増強Lv3"],
      tips: "氷床エリアでは自分の移動速度も下がるため位置取りが重要。高速突進後に必ず隙が生まれるのでそこを狙う。翼膜が弱点部位。",
      mainRewards: ["ベリオロスの剛爪", "ベリオロスの上鱗"],
      rareRewards: ["竜玉"]
    },
    {
      id: 4,
      monster: "ドスジャギィ",
      icon: "🦎",
      startDate: "2026-05-18",
      endDate: "2026-05-25",
      isActive: true,
      starRating: 2,
      element: "なし",
      weaknesses: {
        fire:    1,
        water:   0,
        thunder: 2,
        ice:     1,
        dragon:  0
      },
      recommendedElement: "雷",
      keySkills: ["体力増強Lv2", "攻撃Lv3"],
      tips: "仲間を呼ぶ前に素早く倒すのが基本。雷属性武器が特に有効。呼び出したジャギィノスは無視してボス一点集中でOK。",
      mainRewards: ["ジャギィの鱗", "とがった爪"],
      rareRewards: ["大きな骨"]
    }
  ],

  // ==============================================================
  //  拠点要撃戦セクション
  //  checklist の priority: "high"=必須 / "medium"=推奨 / "low"=任意
  //  recommendedBuilds の color: "red" / "blue" / "green"
  // ==============================================================
  defense: {
    // 現在の開催情報
    current: {
      title: "拠点要撃戦：鉄壁の守護 第3波",
      season: "シーズン2",
      endDate: "2026-06-01",
      difficulty: "★★★★",
      targetMonsters: ["ジャギィ × 多数", "ジャギィノス × 少数", "ドスジャギィ（ボス）"],
      description: "序盤の雑魚を素早くさばき、ドスジャギィのボス戦に備えよう。拠点HPの管理が勝敗を分ける。",
      rewards: ["操虫棍専用素材", "レア装飾品", "シーズンポイント×3"]
    },

    // 出発前チェックリスト（チェックした内容はスマホでも保存される）
    checklist: [
      { item: "大回復薬グレートを10本以上用意する",     priority: "high",   category: "アイテム" },
      { item: "大タル爆弾Gを5個以上用意する",           priority: "high",   category: "アイテム" },
      { item: "こんがり肉（体力上限UP）を食べておく",   priority: "high",   category: "アイテム" },
      { item: "武器の斬れ味・強化レベルを最大にする",   priority: "high",   category: "武器" },
      { item: "属性耐性（雷）を合計30以上にする",       priority: "medium", category: "防具" },
      { item: "耐震スキルが付いているか確認する",       priority: "medium", category: "スキル" },
      { item: "仲間と役割分担（アタッカー/サポート）を決める", priority: "medium", category: "作戦" },
      { item: "回線・通信環境を安定させる",             priority: "low",    category: "環境" }
    ],

    // 役割別推奨ビルド
    recommendedBuilds: [
      {
        role: "アタッカー",
        icon: "⚔️",
        weapon: "大剣 / 片手剣",
        skills: ["弱点特攻Lv3", "集中Lv3", "超会心Lv3", "体力増強Lv2"],
        color: "red",
        notes: "ボスに集中して一気にダメージを出す役割。雑魚には手を出さず火力を温存しておくのが理想。"
      },
      {
        role: "サポート",
        icon: "🛡️",
        weapon: "ランス / ガンランス",
        skills: ["ガード強化Lv3", "体力増強Lv3", "不屈Lv1", "砲術Lv2"],
        color: "blue",
        notes: "拠点前に陣取り雑魚を処理しながら守る役割。ボス戦でも盾役として味方の被弾を減らす。"
      },
      {
        role: "速攻",
        icon: "💨",
        weapon: "双剣 / 操虫棍",
        skills: ["回避性能Lv3", "体力増強Lv3", "属性攻撃強化Lv5", "スタミナ急速回復Lv2"],
        color: "green",
        notes: "雑魚を素早く処理して拠点へのプレッシャーを下げる役割。立ち回りの上手さが求められる。"
      }
    ],

    // 攻略のコツ（番号順に表示）
    generalTips: [
      "拠点のHPゲージを常に意識し、残り20%を切ったら全員で防御に集中",
      "大型モンスターが出現したら全員でフォーカスして最優先で討伐する",
      "回復アイテムはケチらず、HPが50%を下回ったらすぐに使う",
      "序盤は体力消費を抑えてアイテムを温存し、終盤ボス戦に備える",
      "ボスの大技（予備動作あり）を覚えて回避できると被弾が激減する",
      "ソロ攻略時はサポートビルドで粘り強く立ち回るのがおすすめ"
    ]
  }

}
