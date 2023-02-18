import re

_forbidden_input_rates = [
    ('*', 2),
    ('"', 2),
    (';', 4),
    (',', 2),
    ('INSERT', 4),
    ('INTO', 2),
    ('SELECT', 4),
    ('FROM', 2),
    ('UPDATE', 4),
    ('DELETE', 8),
    ('WHERE', 2),
    ('DISTINCT', 4),
    ('GROUP BY', 4),
    ('ORDER BY', 4),
    ('HAVING', 4),
    ('DROP', 16),
    ('TABLE', 16),
    ('COUNT(', 8),
    ('SUM(', 8),
    ('MIN(', 8),
    ('MAX(', 8),
    ('BETWEEN', 4),
    ('LIKE', 2),
    ('UPPER(', 8),
    ('LOWER(', 8),
    ('COALESCE', 8),
    ('LIMIT', 4),
    ('OFFSET', 8),
    ('VALUES', 4),
    ('SET', 2, 'UPDATE', 8)
]


def _calculate_forbidden_score_sql(input_value: str):
    score_total = 1
    for index, rate in enumerate(_forbidden_input_rates):
        if input_value.upper().find(rate[0]) > -1:
            if index < 4:
                score_total *= rate[1]
            elif rate[0] == 'SET' and input_value.upper().find(rate[2]):
                score_total *= rate[3]
            else:
                score_total *= rate[1]
    return score_total


def _calculate_forbidden_score_xss(input_value: str):
    patterns = [re.compile(
        "<[a-zA-Z]{1,9}[1-9]{0,2}>"), re.compile("</[a-zA-Z]{1,9}[1-9]{0,2}>")]
    results = [1 if p.search(input_value) else 0 for p in patterns]
    return sum(results)


def input_validation(input_value: str):
    sql_injection_hazard_rate = _calculate_forbidden_score_sql(input_value)
    xss_hazard_rate = _calculate_forbidden_score_xss(input_value)
    return bool(sql_injection_hazard_rate > 32) or bool(xss_hazard_rate > 0)


def _password_validation(input_value: str):
    return bool(input_value is not None and len(input_value) >= 8)


def _username_validation(input_value: str):
    return bool(input_value is not None and len(input_value) >= 5)


def validate_reg_or_log(input_value: str, validation: str):
    if validation == "PASSWORD":
        return _password_validation(input_value)
    return _username_validation(input_value)

# testing strings
# print(input_validation('"INSERT INTO Users (uname, pwhash) VALUES (\'hohoo\',\'hahaa\')";'))
# print(input_validation('"DROP TABLE Users";'))
# print(input_validation('incase this fails, drop it'))
# print(input_validation('"SELECT * FROM Users ORDER BY uname ASC";'))
# print(input_validation('<script>function() {"DROP TABLE Users";}</>'))
# print(input_validation('<ul><li>first one to drop</li></ul>'))
# print(input_validation('<script>function() {"UPDATE Users SET pw_hash=\'pwned\'";}</script>'))
