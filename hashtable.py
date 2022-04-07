from math import floor


class HashTable:

    def __init__(self, init_size):
        # Initializes the underlying list
        # Upsizes the init size using the 70/30 rule for collision avoidance
        self.__base_list = [None] * floor(init_size * 1.42)

    # Returns the index in base array of hashed key
    def __hash_key(self, key):
        return hash(key) % len(self.__base_list)

    def __new_pair(self, index, key, value):
        self.__base_list[index].append(key)
        self.__base_list[index].append(value)

    def put(self, key, value):
        # Gets index of key
        index = self.__hash_key(key)

        # Checks for existing entry(collision)
        if self.__base_list[index] is None:
            self.__base_list[index] = []
            self.__new_pair(index, key, value)

        else:
            for k in range(0, len(self.__base_list[index]), 2):
                if self.__base_list[index][k] == key:
                    self.__base_list[index][k + 1] = value
                    return

            self.__new_pair(index, key, value)

    def get(self, key):
        # Gets index of key
        index = self.__hash_key(key)

        # Returns None if entry does not exist for given key
        if self.__base_list[index] is None:
            return None

        elif len(self.__base_list[index]) == 2:
            return self.__base_list[index][1]

        else:
            for k in range(0, len(self.__base_list[index]), 2):
                if self.__base_list[index][k] == key:
                    return self.__base_list[index][k + 1]

            return None

    def all(self):
        found = []
        for i in range(0, len(self.__base_list) ):
            if self.__base_list[i] is not None:

                if len(self.__base_list[i]) == 2:
                    found.append((self.__base_list[i][0],self.__base_list[i][1]))

                else:
                    for k in range(0, len(self.__base_list[i]), 2):
                        found.append((self.__base_list[i][k], self.__base_list[i][k +1 ]))

        return found

    def remove(self, key):
        index = self.__hash_key(key)

        if self.__base_list[index] is None:
            return None

        elif len(self.__base_list[index]) == 2:
            self.__base_list[index] = None

        else:
            for k in range(0, len(self.__base_list[index]), 2):
                if self.__base_list[index][k] == key:
                    self.__base_list[index][k] = None
                    self.__base_list[index][k + 1] = None

            return None
