# LearningPythonLab

## ブランチ命名ルール

このプロジェクトでは、作業内容に応じて以下の命名規則に従ってブランチ名をつけます。これにより、プロジェクトが整理され、作業内容が一目でわかるようにします。

### 1. 学習

特定のライブラリや技術の学習を行う場合、以下のルールに従ってブランチ名をつけます。

#### 命名パターン:

- `learning/[ライブラリ名または学習内容]/day-[番号]`  
  **例:** `learning/pytest/day-1`, `learning/django/day-2`
  
- **ホットフィックス・バグ修正**
  - `learning/[ライブラリ名]/hotfix/[修正内容]`  
    **例:** `learning/pytest/hotfix/fix-test-error`, `learning/django/hotfix/fix-setup-bug`
  
- **リファクタリング**
  - `learning/[ライブラリ名]/refactor/[改善内容]`  
    **例:** `learning/pytest/refactor/improve-test-cases`, `learning/django/refactor/clean-code`

---

### 2. 演習・チュートリアル

チュートリアルや演習問題に取り組む際に使用します。

#### 命名パターン:

- `exercise/[ライブラリ名または内容]/day-[番号]`  
  **例:** `exercise/pytest/day-1`, `exercise/django/day-2`
  
- **ホットフィックス・バグ修正**
  - `exercise/[ライブラリ名]/hotfix/[修正内容]`  
    **例:** `exercise/pytest/hotfix/fix-import-error`, `exercise/django/hotfix/fix-migration-error`
  
- **リファクタリング**
  - `exercise/[ライブラリ名]/refactor/[改善内容]`  
    **例:** `exercise/pytest/refactor/improve-performance`, `exercise/django/refactor/refactor-routes`

---

### 3. プロジェクト

新しいプロジェクトやアプリケーションの開発に使用します。

#### 命名パターン:

- **機能追加**
  - `project/[プロジェクト名]/feature/[機能名]`  
    **例:** `project/todo-app/feature/add-login`, `project/blog-app/feature/add-comments`
  
- **ホットフィックス・バグ修正**
  - `project/[プロジェクト名]/hotfix/[修正内容]`  
    **例:** `project/todo-app/hotfix/fix-login-error`, `project/blog-app/hotfix/fix-post-bug`
  
- **リファクタリング**
  - `project/[プロジェクト名]/refactor/[改善内容]`  
    **例:** `project/todo-app/refactor/improve-ui`, `project/blog-app/refactor/clean-models`

---

### 4. アイディア・実験

新しいアイディアや機能を試す際に使用します。

#### 命名パターン:

- **機能追加**
  - `experiment/[アイディア名]/feature/[機能名]`  
    **例:** `experiment/new-algorithm/feature/add-sorting`, `experiment/chat-app/feature/add-encryption`
  
- **ホットフィックス・バグ修正**
  - `experiment/[アイディア名]/hotfix/[修正内容]`  
    **例:** `experiment/new-algorithm/hotfix/fix-sorting-error`, `experiment/chat-app/hotfix/fix-connection-issue`
  
- **リファクタリング**
  - `experiment/[アイディア名]/refactor/[改善内容]`  
    **例:** `experiment/new-algorithm/refactor/improve-performance`, `experiment/chat-app/refactor/clean-code`

---

### まとめ

この命名規則を守ることで、作業内容が整理され、チームメンバーや自分自身がブランチの目的を簡単に理解できるようになります。各ブランチの命名は、ブランチの目的（学習、演習、プロジェクト、アイディア）に応じて明確に定義されており、開発プロセスの効率化に貢献します。
