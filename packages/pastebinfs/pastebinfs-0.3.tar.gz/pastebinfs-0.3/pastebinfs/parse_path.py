def parse_path(path: str) -> str: 
    while path[0] == '/':
        path = path[1:]

    return path.strip()