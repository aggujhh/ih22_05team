from dbutils.pooled_db import PooledDB
import pymysql
import threading


class SqlPool(object):
    def __init__(self):
        self.pool = PooledDB(
            creator=pymysql,  # 使用するデータベースモジュール
            maxconnections=6,  # 接続プールで許可される最大接続数
            mincached=2,  # 初期化時、接続プールで作成される最小空き接続数
            blocking=True,  # 接続プールに利用可能な接続がない場合、待機するかどうか
            host='localhost',
            port=3306,
            user='root',
            password='',
            database='ih22_db',
            charset='utf8',
            autocommit=True  # データを自動コミットする
        )
        self.local = threading.local()

    def open(self):
        # 接続プールから接続と対応するカーソルを取得
        conn = self.pool.connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)  # 結果を辞書で返す、デフォルトはタプル
        return conn, cursor

    def close(self, conn, cursor):
        # 接続とカーソルを閉じる
        conn.close()
        cursor.close()

    # クエリを実行し、最初のレコードを返す
    def fetchone(self, sql, *args):
        conn, cursor = self.open()
        cursor.execute(sql, args)
        result = cursor.fetchone()
        self.close(conn, cursor)
        return result

    # クエリを実行し、すべてのレコードを返す
    def fetchall(self, sql, *args):
        conn, cursor = self.open()
        cursor.execute(sql, args)
        result = cursor.fetchall()
        self.close(conn, cursor)
        return result

    # 挿入操作を実行し、影響を受けた行数を返す
    def insert(self, sql, *args):
        conn, cursor = self.open()
        cursor.execute(sql, args)
        result = cursor.rowcount  # 実際に更新された行数を取得
        self.close(conn, cursor)
        return result

    # コンテキストマネージャのサポート
    def __enter__(self):
        conn, cursor = self.open()
        # ======================================================================
        # Pythonのgetattr関数を使用して、self.localオブジェクトから"stack"という属性を取得しようとしています。
        # これはthreading.local()のインスタンスです。
        # 属性が存在しない場合はgetattrの第3引数、ここではNoneを返します。
        # ======================================================================
        rv = getattr(self.local, "stack", None)
        if not rv:
            self.local.stack = [(conn, cursor), ]  # スタックを初期化
        else:
            self.local.stack.append((conn, cursor))  # スタックに追加
        return cursor

    # コンテキストマネージャの終了操作をサポート
    def __exit__(self, exc_type, exc_val, exc_tb):
        rv = getattr(self.local, "stack", None)
        if not rv:
            del self.local.stack  # スタックを削除
            return
        conn, cursor = rv.pop()  # 最後の要素をポップ
        self.close(conn, cursor)  # 接続とカーソルを閉じる


# シングルトンパターン
db = SqlPool()
