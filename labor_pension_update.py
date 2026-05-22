from config import DBhost, DBname, DBuser, DBpwd
import MySQLdb
import pandas as pd
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_db_connection():
    try:
        conn = MySQLdb.connect(
            host=DBhost,
            user=DBuser,
            password=DBpwd,
            db=DBname,
            charset='utf8mb4'
        )
        return conn
    except MySQLdb.Error as e:
        logger.error(f"DB connection failed: {e}")
        raise


def read_csv_into_df(csv_path):
    try:
        df = pd.read_csv(csv_path, sep=',', encoding='big5')
        return df
    except Exception as e:
        logger.error(f"Failed to read CSV: {e}")
        raise


def get_users_ssn(df):
    try:
        return tuple(row.ssn for row in df.itertuples(index=False))
    except Exception as e:
        logger.error(f"Error extracting SSNs: {e}")
        raise


def get_percentage_mapping(df):
    try:
        return {row.ssn: row.percentage for row in df.itertuples(index=False)}
    except Exception as e:
        logger.error(f"Error building percentage mapping: {e}")
        raise

def update_labor_pension(conn, conn_cur, df):
    try:
        user_ssns = get_users_ssn(df)

        if not user_ssns:
            logger.warning("No SSNs found in input file")
            return

        placeholders = ', '.join(['%s'] * len(user_ssns))

        get_users_sql = f"""
            SELECT *
            FROM nca_db.現役役籍資料_999
            WHERE 身分證字號 IN ({placeholders})
        """

        conn_cur.execute(get_users_sql, user_ssns)
        db_rows = conn_cur.fetchall()

        if len(user_ssns) != len(db_rows):
            logger.warning("Input file and DB user count mismatch")
            raise ValueError("User count mismatch")

        percentage_mapping = get_percentage_mapping(df)

        update_sql = """
            UPDATE nca_db.現役役籍資料_999
            SET 自提勞退 = %s
            WHERE 身分證字號 = %s
        """

        for ssn in user_ssns:
            percentage = percentage_mapping[ssn]

            try:
                conn_cur.execute(update_sql, (percentage, ssn))
                logger.info(f"Updated {ssn} -> {percentage}")
            except MySQLdb.Error as e:
                logger.error(f"Failed updating {ssn}: {e}")
                raise

        conn.commit()
        logger.info("All updates committed successfully")

    except Exception as e:
        conn.rollback()
        logger.error(f"Transaction failed, rolled back: {e}")
        raise

def main():
    conn = None
    conn_cur = None

    try:
        conn = get_db_connection()
        conn_cur = conn.cursor()

        df = read_csv_into_df('./labor_pension_mock.csv')
        update_labor_pension(conn, conn_cur, df)

    except Exception as e:
        logger.error(f"Program failed: {e}")
        sys.exit(1)

    finally:
        if conn_cur:
            conn_cur.close()
        if conn:
            conn.close()
        logger.info("DB connection closed")


if __name__ == "__main__":
    main()