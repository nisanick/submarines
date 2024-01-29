class Part:

    surveillance = 0
    retrieval = 0
    speed = 0
    range = 0
    favor = 0
    cost = 0

    def __init__(self, surveillance, retrieval, speed, range, favor, cost) -> None:
        self.surveillance = surveillance
        self.retrieval = retrieval
        self.speed = speed
        self.range = range
        self.favor = favor
        self.cost = cost


