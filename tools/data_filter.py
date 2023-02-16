
_filtering_modes = ["ALL","PUBLIC","LOGIN","AGE","SECURITY"]

def filter_chats(chats:list, filtering:str):
    if filtering not in _filtering_modes:
        return None
    if filtering == _filtering_modes[0]:
        return chats
    if filtering == _filtering_modes[1]:
        _filtered = [chat for chat in chats if chat[5] == "NONE"]
        return _filtered
    if filtering == _filtering_modes[2]:
        _filtered = [chat for chat in chats if chat[5] == "LOGIN"]
        return _filtered
    if filtering == _filtering_modes[3]:
        _filtered = [chat for chat in chats if chat[5] == "AGE"]
        return _filtered
    if filtering == _filtering_modes[4]:
        _filtered = [chat for chat in chats if chat[5] == "SEC"]
        return _filtered