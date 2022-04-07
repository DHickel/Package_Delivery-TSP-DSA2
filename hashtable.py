from math import floor


class HashTable:

    def __init__(self, init_size):
        # Initializes the underlying list
        # Upsizes the init size using the 70/30 rule for collision avoidance
        self.__base_list = [None] * floor(init_size * 1.42)

    # Returns the index in base array of hashed key
    # "Private" to avoid direct access,which could lead to errors
    def __hash_key(self, key):
        return hash(key) % len(self.__base_list)

    # Inserts a new key/value pair into the bucket index of the underlying list
    # Keys will always be even, and their value will be i + 1 (odd)
    # "Private" to avoid direct access, which could lead to errors
    def __new_pair(self, index, key, value):
        self.__base_list[index].append(key)
        self.__base_list[index].append(value)

    # Function for inserting a key/value into the hashtable

    def put(self, key, value):
        # Gets index of key
        index = self.__hash_key(key)

        # Checks for existing entry(collision) if not found inits the chaining list for that bucket and adds key/value pair
        if self.__base_list[index] is None:
            self.__base_list[index] = []
            self.__new_pair(index, key, value)

        # If collision is found, check if it is an update to an existing key and updates
        # else it appends a new pair to the bucket list
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

        # If bucket only has a single key/value pair, directly access them by index.
        # This imparts a small speed up on most lookups(single bucket entries) versus a loop search
        elif len(self.__base_list[index]) == 2:
            return self.__base_list[index][1]

        # Uses a loop to search the bucket list if it contains multiple key/value pairs
        else:
            for k in range(0, len(self.__base_list[index]), 2):
                if self.__base_list[index][k] == key:
                    return self.__base_list[index][k + 1]

            return None

    # Loops through all indexes of the underlying list to return a tuple list of all contained values
    def all(self):
        found = []
        for i in range(0, len(self.__base_list) ):
            if self.__base_list[i] is not None:

                # Direct access speed up, for single key/value buckets
                if len(self.__base_list[i]) == 2:
                    found.append((self.__base_list[i][0],self.__base_list[i][1]))

                # Loops through bucket to get all key/value pairs if there are multiple
                else:
                    for k in range(0, len(self.__base_list[i]), 2):
                        found.append((self.__base_list[i][k], self.__base_list[i][k +1 ]))
        return found

    def remove(self, key):
        # Gets index of key
        index = self.__hash_key(key)

        # Returns None if entry does not exist for given key
        if self.__base_list[index] is None:
            return None

        # If only one key/value pair exists, deletes(None) the list object at that bucket
        elif len(self.__base_list[index]) == 2:
            self.__base_list[index] = None

        # If multiple key/value pairs exist, loops through to find the bucket index for the key/value pair to remove
        # Once found deleted their object/values (None)
        else:
            for k in range(0, len(self.__base_list[index]), 2):
                if self.__base_list[index][k] == key:
                    self.__base_list[index][k] = None
                    self.__base_list[index][k + 1] = None


