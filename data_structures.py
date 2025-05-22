class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class CustomList:
    def __init__(self):
        self.head = None
        self._size = 0

    def append(self, value):
        new_node = Node(value)
        if not self.head:
            self.head = new_node
        else:
            curr = self.head
            while curr.next:
                curr = curr.next
            curr.next = new_node
        self._size += 1

    def __len__(self):
        return self._size

    def __iter__(self):
        curr = self.head
        while curr:
            yield curr.value
            curr = curr.next

    def __getitem__(self, index):
        if index < 0 or index >= self._size:
            raise IndexError("Indekss ārpus robežām")
        curr = self.head
        for _ in range(index):
            curr = curr.next
        return curr.value

    def __repr__(self):
        return f"CustomList([{', '.join(repr(x) for x in self)}])"


class CustomDict:
    def __init__(self, initial=None, initial_capacity=16):
        if isinstance(initial, dict):
            mapping = initial
            capacity = initial_capacity
        elif isinstance(initial, int):
            mapping = None
            capacity = initial
        else:
            mapping = None
            capacity = initial_capacity
        self._buckets = [[] for _ in range(capacity)]
        self._size = 0
        if mapping:
            for k, v in mapping.items():
                self[k] = v

    def _bucket(self, key):
        return self._buckets[hash(key) % len(self._buckets)]

    def __setitem__(self, key, value):
        bucket = self._bucket(key)
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self._size += 1

    def __getitem__(self, key):
        bucket = self._bucket(key)
        for k, v in bucket:
            if k == key:
                return v
        raise KeyError(key)

    def __contains__(self, key):
        bucket = self._bucket(key)
        return any(k == key for k, _ in bucket)

    def __delitem__(self, key):
        bucket = self._bucket(key)
        for i, (k, _) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self._size -= 1
                return
        raise KeyError(key)

    def keys(self):
        for bucket in self._buckets:
            for k, _ in bucket:
                yield k

    def items(self):
        for bucket in self._buckets:
            for k, v in bucket:
                yield (k, v)

    def values(self):
        for _, v in self.items():
            yield v

    def __len__(self):
        return self._size

    def __repr__(self):
        items = ", ".join(f"{k!r}: {v!r}" for k, v in self.items())
        return f"CustomDict({{{items}}})"

    def __iter__(self):
        return self.keys()


class CustomSet:
    def __init__(self):
        self._dict = CustomDict()

    def add(self, value):
        self._dict[value] = True

    def remove(self, value):
        del self._dict[value]

    def __contains__(self, value):
        return value in self._dict

    def __iter__(self):
        return self._dict.keys()

    def __len__(self):
        return len(self._dict)

    def __repr__(self):
        return f"CustomSet({{ {', '.join(repr(x) for x in self)} }})"
