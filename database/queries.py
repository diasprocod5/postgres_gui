
get_user_roles = "SELECT rolname FROM pg_roles WHERE pg_has_role(current_user, oid, 'member')"


query_dict = {
    'tariffs':"SELECT * FROM tariffs",
    'general':"SELECT * FROM get_client_data()"
}
