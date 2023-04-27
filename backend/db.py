from backend.router import Router
from typing import ByteString
import base64
from sqlalchemy import exc

router = Router()
router.create_table()

def check_post_status(post_url: str, encoded_message: ByteString) -> bool:
        db_conn = router.mysql_conn
        trans = db_conn.begin()
        sql_cmd = f"""
            SELECT pushes
            FROM post
            WHERE url = '{post_url}'
        """
        request_data = db_conn.execute(sql_cmd).first()
        trans.commit()
        if request_data["pushes"] == encoded_message:
            return False
        return True

def save_post_to_db(result_post_obj: dict):
        if result_post_obj.get("valid", False):

            url = result_post_obj["url"]
            slash_index = url.rfind("/")
            primary_key = url[slash_index:]

            author = result_post_obj["author"]
            nick_name_index = author.find('(')
            if nick_name_index != -1:
                author = author[:nick_name_index]
            author_encoded = base64.b64encode(author.encode('utf-8')).decode("utf-8")

            push_message = ""
            for push in result_post_obj.get("push", []):
                push_message += push + "\n"
            pushes_encoded = base64.b64encode(push_message.encode('utf-8')).decode("utf-8")
            
            db_conn = router.mysql_conn
            trans = db_conn.begin()
            try:
                sql_cmd = f"""
                    INSERT INTO post
                    VALUES ('{primary_key}', '{author_encoded}', '{pushes_encoded}', 1)
                """
                db_conn.execute(sql_cmd)
            except exc.SQLAlchemyError as e:
                if check_post_status(primary_key, pushes_encoded):
                    sql_cmd = f"""
                        UPDATE post SET pushes = '{pushes_encoded}', status = 1
                        WHERE url = '{primary_key}'
                    """
                    db_conn.execute(sql_cmd)
                    print(f"{primary_key} updated.")
                else:
                    print(f"{primary_key} is the latest.")
            
            trans.commit()

def request_updated_post():
    db_conn = router.mysql_conn
    trans = db_conn.begin()
    request_sql_cmd = f"""
                        SELECT *
                        FROM post
                        WHERE status = 1
        """
    request_data = db_conn.execute(request_sql_cmd)
    trans.commit()
    return request_data

def update_post_status(url: str):
    db_conn = router.mysql_conn
    trans = db_conn.begin()
    update_sql_cmd = f"""
                        UPDATE post SET status = 0
                        WHERE url = '{url}'
        """
    db_conn.execute(update_sql_cmd)
    trans.commit()