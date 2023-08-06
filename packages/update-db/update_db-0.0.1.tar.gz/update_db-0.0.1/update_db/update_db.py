import logging
from typing import Dict, Optional

import psycopg2
from psycopg2.extras import Json

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def update_db(model_version_id: int, db_info: dict, status: Optional[str] = None, metrics: Optional[Dict] = None):
    conn = None
    try:
        logging.debug("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(
            host=db_info["POSTGRES_HOST"],
            port=db_info["POSTGRES_PORT"],
            database=db_info["POSTGRES_DB_NAME"],
            user=db_info["POSTGRES_USER"],
            password=db_info["POSTGRES_PASSWORD"]
        )
        logging.debug("Connect to DB successfully")
        cur = conn.cursor()
        if status:
            query = """UPDATE "ModelVersions" SET run_status=%s WHERE model_version_id=%s"""
            cur.execute(query, [status, model_version_id])
            conn.commit()

        if metrics:
            logging.debug("Update metrics in DB")
            query = """UPDATE "ModelVersions" SET metrics=%s WHERE model_version_id=%s"""
            cur.execute(query, [Json(metrics), model_version_id])
            conn.commit()

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
