def get_boolean_query_item(request, name):
    query_item = request.query_params.get(name, None)
    if query_item is None:
        return None
    return True if query_item == 'true' else False