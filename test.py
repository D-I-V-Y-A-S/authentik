import ast
def handle_authentik_event():
    # data = request.get_json(force=True, silent=True)  
    data =  {'body': "model_updated: {'model': {'pk': 22, 'app': 'authentik_core', 'name': 'user1', 'model_name': 'user'}, 'http_request': {'args': {}, 'path': '/api/v3/core/users/', 'method': 'POST', 'request_id': 'db414c7a890140138fdf6c1e10ca7ea3', 'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'}}", 'severity': 'alert', 'user_email': 'divya.s@cprime.com', 'user_username': 'divyas', 'event_user_email': 'divya.s@cprime.com', 'event_user_username': 'divyas'}

    body_str = data.get("body", "")
    
    # Convert the string to a Python dict safely
    try:
        # Strip the prefix "model_updated: " and parse the rest
        if body_str.startswith("model_updated: "):
            body_dict = ast.literal_eval(body_str.replace("model_updated: ", "", 1))
            name = body_dict.get("model", {}).get("name")
        else:
            name = None
    except Exception as e:
        print("Error parsing body:", e)
        name = None

    print("Extracted name:", name)


handle_authentik_event()