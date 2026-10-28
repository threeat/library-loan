"""문제지 예시 · 확인표 10줄 · 이상한 값 자체 검증.  실행: python edge_test.py"""
from solution import LibraryLoan

def eq(got, want, what):
    assert got == want, f"{what}: {got!r} != {want!r}"

# 문제지 예시
L = LibraryLoan()
eq(L.borrow("B001", "김철수", 1), True, "ex1"); eq(L.borrow("B001", "이영희", 2), False, "ex2")
eq(L.get_loans("김철수"), [("B001", 15)], "ex3"); eq(L.return_book("B001", "이영희", 5), -1, "ex4")
eq(L.return_book("B001", "김철수", 18), 3, "ex5"); eq(L.borrow("B002", "김철수", 19), False, "ex6")
eq(L.borrow("B002", "김철수", 20), False, "ex6b"); eq(L.borrow("B002", "김철수", 21), True, "ex7")

# 확인표
L = LibraryLoan()
eq(L.borrow("B001", "김민수", 1), True, "1"); eq(L.borrow("B001", "박지은", 2), False, "2")
eq(L.borrow("B002", "김민수", 2), True, "3a"); eq(L.borrow("B003", "김민수", 2), True, "3b")
eq(L.borrow("B004", "김민수", 2), False, "4"); eq(L.borrow("B009", "박지은", 2), False, "5")
eq(L.return_book("B001", "김민수", 10), 0, "6"); eq(L.get_loans("김민수"), [("B002", 16), ("B003", 16)], "7")
eq(L.borrow("B004", "김민수", 20), False, "8")
eq(L.return_book("B002", "김민수", 20), 4, "9a"); eq(L.return_book("B003", "김민수", 20), 4, "9b")
eq(L.borrow("B004", "김민수", 23), False, "10a"); eq(L.borrow("B004", "김민수", 24), True, "10b")

# 이상한 값
L = LibraryLoan()
for d in (0, -1, 2.5, 1.0, True, False, "3", None):
    eq(L.borrow("B001", "가", d), False, f"bad day {d!r}")
for b in ("B000", "B006", "b001", "", None, ["B001"], 1):
    eq(L.borrow(b, "가", 1), False, f"bad book {b!r}")
eq(L.get_loans("가"), [], "nothing changed")
eq(L.borrow("B001", "가", 5), True, "ok")
eq(L.return_book("B001", "가", 4), -1, "return before borrow day")
eq(L.return_book("B001", "가", True), -1, "return bool day"); eq(L.return_book("B001", "가", 6.0), -1, "float day")
eq(L.return_book("B002", "가", 6), -1, "not borrowed"); eq(L.return_book("B009", "가", 6), -1, "no book")
eq(L.return_book("B001", "가", 5), 0, "same day return"); eq(L.return_book("B001", "가", 6), -1, "already returned")
eq(L.borrow("B001", "나", 6), True, "other can borrow after return")
eq(L.get_loans("없는사람"), [], "empty")

# 기한 당일은 연체 아님 / 기한 당일 대출 가능, 다음날 불가
L = LibraryLoan(); L.borrow("B001", "가", 1)
eq(L.borrow("B002", "가", 15), True, "due-day borrow ok"); eq(L.borrow("B003", "가", 16), False, "overdue hold")
eq(L.return_book("B001", "가", 15), 0, "return on due day")

# 정지 기간 겹침: 더 늦게 끝나는 쪽
L = LibraryLoan(); L.borrow("B001", "가", 1); L.borrow("B002", "가", 1)
eq(L.return_book("B001", "가", 25), 10, "10 overdue")   # 25~34 정지
eq(L.return_book("B002", "가", 26), 11, "11 overdue")   # 26~36 정지
eq(L.borrow("B003", "가", 36), False, "still suspended"); eq(L.borrow("B003", "가", 37), True, "free 37")
L = LibraryLoan(); L.borrow("B001", "가", 1); L.borrow("B002", "가", 1)
eq(L.return_book("B001", "가", 25), 10, "a"); eq(L.return_book("B002", "가", 25), 10, "b (not added)")
eq(L.borrow("B003", "가", 35), True, "same period not summed")
# 정지는 그 사람만
eq(L.borrow("B004", "나", 26), True, "other person unaffected")

# 정렬: 같은 기한이면 책 번호 순
L = LibraryLoan(); L.borrow("B005", "가", 3); L.borrow("B002", "가", 3); L.borrow("B004", "가", 1)
eq(L.get_loans("가"), [("B004", 15), ("B002", 17), ("B005", 17)], "sort")
eq(L.borrow("B001", "가", 3), False, "max 3")
print("edge_test: 모두 통과")
