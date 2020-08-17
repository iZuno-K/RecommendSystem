def make_response_two_ai(json_dict):
    responses = [json_dict["#chat_{}".format(len(json_dict) - 1)] + "はちょっと...",
                 json_dict["#chat_{}".format(len(json_dict) - 1)] + "はお勧め",
                 "まあそう言わないで",
                 "いやいういう"]
    _classes = ['talk_left1', 'talk_left2', 'talk_left1', 'talk_left2']
    return responses, _classes
