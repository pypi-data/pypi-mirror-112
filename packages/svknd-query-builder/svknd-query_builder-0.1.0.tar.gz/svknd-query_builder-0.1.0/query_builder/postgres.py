def create(data, table):
    return "INSERT INTO " + table + " (" + ", ".join(data.keys()) + ") VALUES (" + ", ".join(
        ["%(" + k + ")s" for k in data]) + ")"


def update(data, table):
    maps = []
    for d in data:
        maps.append(d + " = %(" + d + ")s")
    return "UPDATE " + table + " SET " + ", ".join(maps) + " WHERE id='{}'".format(data['id'])
