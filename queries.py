SQL_QUERY = {
    "register_data": "insert into {0} values('{1}', '{2}', '{3}')",
    "load_data": "insert into {0} values({1})",
    "refresh": "delete from auth where Created <= CURRENT_DATE - INTERVAL '5 day'",
    "auth_query": "SELECT id FROM {0} WHERE id = '{1}'",
    "filter_query": "SELECT distinct {0} from {1}",
    "filter_where_query": "SELECT distinct {0} from {1} where {2}"
}

PSQL_QUERY = {
    "insert_data": "INSERT INTO filter_data VALUES ('{}')",
    "filter_query": "select distinct {0} from filter_data",
    "filter_where_query": "select distinct {0} from filter_data where {1}"
}
