from dbutils.pooled_db import PooledDB
import pymysql
import threading
from routes import logger

class SqlPool(object):
    def __init__(self):
        self.pool = PooledDB(
            creator=pymysql,
            maxconnections=6,
            mincached=2,
            blocking=True,
            host='localhost',
            port=3306,
            user='ih05team',
            password='ih05_123456',
            database='ih22_db',
            charset='utf8',
            autocommit=False  # データの自動コミットをオフにする
        )
        self.local = threading.local()

    def open(self):
        conn = self.pool.connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        return conn, cursor

    def close(self, conn, cursor):
        cursor.close()
        conn.close()

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

    # トランザクションの開始
    def begin_transaction(self):
        conn, cursor = self.open()
        conn.begin()
        self.local.conn = conn
        self.local.cursor = cursor

    # トランザクションのコミット
    def commit(self):
        if hasattr(self.local, "conn"):
            self.local.conn.commit()
            logger.info("commit成功しました。")
            self.close(self.local.conn, self.local.cursor)  # トランザクション終了後に接続を閉じる
            del self.local.conn
            del self.local.cursor

    # トランザクションのロールバック
    def rollback(self):
        if hasattr(self.local, "conn"):
            self.local.conn.rollback()
            logger.error("commit失敗し、rollbackする。")  # 添加错误日志
            self.close(self.local.conn, self.local.cursor)
            del self.local.conn
            del self.local.cursor

    # コンテキストマネージャのサポート
    def __enter__(self):
        self.begin_transaction()
        return self.local.cursor  # コンテキスト内で cursor を直接使用

    # コンテキストマネージャの終了操作をサポート
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:  # エラーが発生した場合
            self.rollback()
        else:
            self.commit()  # 正常終了の場合はコミット


# シングルトンパターン
db = SqlPool()
