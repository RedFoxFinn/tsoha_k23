
from tools.database_module import DB

REQUEST_FETCH_SQL = "SELECT R.id AS id,\
                            R.datatime_of_request AS created,\
                            R.info_table AS table,\
                            R.info_id AS entry,\
                            R.change_type,\
                            R.change_info AS info,\
                            U.id AS uid,\
                            U.uname AS uname \
                    FROM Requests R LEFT JOIN Users U \
                    ON R.user_id=U.id"

def get_requests():
    _sql = f"{REQUEST_FETCH_SQL} ORDER BY created ASC"
    _result = DB.session.execute(_sql)  # pylint: disable=no-member
    _data = _result.fetchall()
    return _data


def count():
    """
        module function to return number of entries in the database
        related to the model 'Request'
    """
    _sql = "SELECT count(*) FROM Requests"
    _result = DB.session.execute(_sql)  # pylint: disable=no-member
    _data = _result.fetchall()[0]
    return _data[0]
