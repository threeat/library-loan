# 도서관 대출 시스템 — 아래 클래스를 완성하세요. (클래스·메서드 이름은 바꾸지 마세요)

BOOKS = ("B001", "B002", "B003", "B004", "B005")
LOAN_DAYS = 14
MAX_LOANS = 3


def _valid_day(day):
    # 1 이상의 정수만 허용 (True/False는 정수로 보지 않음)
    return type(day) is int and day >= 1


def _valid_name(name):
    return isinstance(name, str) and name.strip() != ""


class LibraryLoan:
    def __init__(self):
        self.loans = {}       # book_id -> (name, 빌린 날)
        self.suspensions = {}  # name -> [(정지 시작일, 정지 마지막일), ...]

    def _due(self, book_id):
        return self.loans[book_id][1] + LOAN_DAYS

    def _books_of(self, name):
        return [b for b, (who, _) in self.loans.items() if who == name]

    def _suspended(self, name, day):
        return any(s <= day <= e for s, e in self.suspensions.get(name, []))

    def borrow(self, book_id, name, day):
        if book_id not in BOOKS or not _valid_day(day) or not _valid_name(name):
            return False
        if book_id in self.loans:
            return False
        held = self._books_of(name)
        if len(held) >= MAX_LOANS:
            return False
        if any(day > self._due(b) for b in held):
            return False
        if self._suspended(name, day):
            return False
        self.loans[book_id] = (name, day)
        return True

    def return_book(self, book_id, name, day):
        if book_id not in BOOKS or not _valid_day(day) or not _valid_name(name):
            return -1
        if book_id not in self.loans:
            return -1
        who, borrowed = self.loans[book_id]
        if who != name or day < borrowed:
            return -1
        overdue = max(0, day - (borrowed + LOAN_DAYS))
        del self.loans[book_id]
        if overdue > 0:
            # 반납한 날부터 연체 일수만큼 대출 정지. 겹치면 합치지 않고 각 기간을 그대로 둠
            # → 결과적으로 더 늦게 끝나는 쪽까지 정지됨
            self.suspensions.setdefault(name, []).append((day, day + overdue - 1))
        return overdue

    def get_loans(self, name):
        return sorted(((b, self._due(b)) for b in self._books_of(name)),
                      key=lambda t: (t[1], t[0]))
