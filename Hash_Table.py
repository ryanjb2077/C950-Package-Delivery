class Hash_Table_Int:

    def __init__(self, key, item):
        self.key = key
        self.item = item


class Hash_Map:

    # Constructor
    # Creates array length 40 filled with empty lists
    def __init__(self, package_estimate=40):

        self.map = []
        for index in range(package_estimate):
            self.map.append([])

    # Returns  converted key into array index
    def _get_hash(self, key):

        bucket = int(key) % len(self.map)
        return bucket

    # Inserts key and value into bucket
    def insert_value(self, key, value):

        key_hash = self._get_hash(key)
        key_value = [key, value]

        if self.map[key_hash] is None:
            self.map[key_hash] = list([key_value])
            return True

        else:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    pair[1] = key_value
                    return True
            self.map[key_hash].append(key_value)
            return True

    # replaces bucket with new values
    def update(self, key, value):
        key_hash = self._get_hash(key)
        if self.map[key_hash] is not None:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
        else:
            print('Update failed: ' + key)

    # Grab a value from the hash table
    def get(self, key):

        key_hash = self._get_hash(key)
        if self.map[key_hash] is not None:

            for pair in self.map[key_hash]:

                if pair[0] == key:

                    return pair[1]

        return None

    # Remove a value from the hash table
    def delete(self, key):
        key_hash = self._get_hash(key)

        if self.map[key_hash] is None:
            return False

        for i in range(0, len(self.map[key_hash])):

            if self.map[key_hash][i][0] == key:

                self.map[key_hash].pop(i)

                return True

        return False
