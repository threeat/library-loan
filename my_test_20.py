"""블라인드 테스트를 흉내 낸 임의 샘플 20개.  실행: python my_test_20.py
정답은 문제지 규칙으로 직접 계산한 값입니다."""
from solution import LibraryLoan


def eq(got, want, what):
    assert got == want, f"{what} → {got!r}, 정답 {want!r}"


def t01():
    "없는 책 번호 → False"
    L = LibraryLoan()
    eq(L.borrow("B006", "김", 1), False, "B006")
    eq(L.borrow("B000", "김", 1), False, "B000")


def t02():
    "0일째·음수 날짜 대출 → False"
    L = LibraryLoan()
    eq(L.borrow("B001", "김", 0), False, "day 0")
    eq(L.borrow("B001", "김", -3), False, "day -3")


def t03():
    "소수·문자 날짜 대출 → False"
    L = LibraryLoan()
    eq(L.borrow("B001", "김", 2.5), False, "day 2.5")
    eq(L.borrow("B001", "김", 3.0), False, "day 3.0")
    eq(L.borrow("B001", "김", "3"), False, "day '3'")


def t04():
    "True/False 날짜 → 대출·반납 모두 실패"
    L = LibraryLoan()
    eq(L.borrow("B001", "김", True), False, "borrow True")
    eq(L.borrow("B001", "김", False), False, "borrow False")
    L.borrow("B001", "김", 1)
    eq(L.return_book("B001", "김", True), -1, "return True")


def t05():
    "1인 3권까지 → 4권째 False"
    L = LibraryLoan()
    for b in ("B001", "B002", "B003"):
        eq(L.borrow(b, "김", 1), True, b)
    eq(L.borrow("B004", "김", 1), False, "4번째")
    eq(L.borrow("B004", "이", 1), True, "다른 사람은 가능")


def t06():
    "한 권 반납하면 다시 3권째 대출 가능"
    L = LibraryLoan()
    for b in ("B001", "B002", "B003"):
        L.borrow(b, "김", 1)
    eq(L.return_book("B002", "김", 5), 0, "반납")
    eq(L.borrow("B004", "김", 5), True, "다시 대출")


def t07():
    "기한 지난 책 보유 → 기한 당일은 가능, 다음 날 실패"
    L = LibraryLoan()
    L.borrow("B001", "김", 1)                       # 기한 15
    eq(L.borrow("B002", "김", 16), False, "16일째")
    eq(L.borrow("B002", "김", 15), True, "15일째")


def t08():
    "연체 일수 계산 (기한 당일 0, 이후 day-기한)"
    L = LibraryLoan()
    L.borrow("B001", "김", 1); L.borrow("B002", "김", 1)
    eq(L.return_book("B001", "김", 15), 0, "기한 당일")
    eq(L.return_book("B002", "김", 20), 5, "5일 연체")


def t09():
    "남이 빌린 책 반납 → -1, 원래 대출은 유지"
    L = LibraryLoan()
    L.borrow("B001", "김", 1)
    eq(L.return_book("B001", "이", 3), -1, "이영희 반납")
    eq(L.get_loans("김"), [("B001", 15)], "김 목록 유지")


def t10():
    "빌리지 않은 책 / 없는 책 반납 → -1"
    L = LibraryLoan()
    eq(L.return_book("B003", "김", 3), -1, "안 빌린 책")
    eq(L.return_book("B009", "김", 3), -1, "없는 책")


def t11():
    "이미 반납한 책 다시 반납 → -1"
    L = LibraryLoan()
    L.borrow("B001", "김", 1)
    eq(L.return_book("B001", "김", 3), 0, "첫 반납")
    eq(L.return_book("B001", "김", 4), -1, "두 번째 반납")


def t12():
    "빌린 날보다 이른 반납 → -1, 같은 날 반납은 0"
    L = LibraryLoan()
    L.borrow("B001", "김", 10)
    eq(L.return_book("B001", "김", 9), -1, "9일째")
    eq(L.return_book("B001", "김", 10), 0, "10일째")


def t13():
    "이상한 날짜로 반납 실패 → 아무것도 안 바뀜"
    L = LibraryLoan()
    L.borrow("B001", "김", 1)
    eq(L.return_book("B001", "김", 0), -1, "0일째")
    eq(L.return_book("B001", "김", 2.5), -1, "2.5일째")
    eq(L.get_loans("김"), [("B001", 15)], "그대로 대출 중")
    eq(L.borrow("B001", "이", 3), False, "남은 못 빌림")


def t14():
    "문제지 예시: 3일 연체 → 18·19·20일째 정지, 21일째 가능"
    L = LibraryLoan()
    L.borrow("B001", "김", 1)
    eq(L.return_book("B001", "김", 18), 3, "반납")
    eq(L.borrow("B002", "김", 18), False, "18일째")
    eq(L.borrow("B002", "김", 20), False, "20일째")
    eq(L.borrow("B002", "김", 21), True, "21일째")


def t15():
    "정지는 그 사람에게만 적용, 반납한 책은 남이 빌릴 수 있음"
    L = LibraryLoan()
    L.borrow("B001", "김", 1)
    L.return_book("B001", "김", 18)
    eq(L.borrow("B001", "이", 18), True, "이영희 대출")


def t16():
    "정지 중에도 반납 가능 + 겹치면 늦게 끝나는 쪽"
    L = LibraryLoan()
    L.borrow("B001", "김", 1); L.borrow("B002", "김", 1)
    eq(L.return_book("B001", "김", 20), 5, "20~24 정지")
    eq(L.return_book("B002", "김", 22), 7, "정지 중 반납 → 22~28 정지")
    eq(L.borrow("B003", "김", 28), False, "28일째")
    eq(L.borrow("B003", "김", 29), True, "29일째")


def t17():
    "겹칠 때 먼저 받은 정지가 더 늦게 끝나면 그쪽을 따름 (더하지 않음)"
    L = LibraryLoan()
    L.borrow("B001", "김", 1); L.borrow("B002", "김", 10)
    eq(L.return_book("B001", "김", 30), 15, "30~44 정지")
    eq(L.return_book("B002", "김", 31), 7, "31~37 정지")
    eq(L.borrow("B003", "김", 44), False, "44일째")
    eq(L.borrow("B003", "김", 45), True, "45일째 (더했으면 실패)")


def t18():
    "대출 목록: 기한 순, 같으면 책 번호 순"
    L = LibraryLoan()
    L.borrow("B005", "김", 3); L.borrow("B002", "김", 3); L.borrow("B004", "김", 1)
    eq(L.get_loans("김"), [("B004", 15), ("B002", 17), ("B005", 17)], "정렬")


def t19():
    "날짜 순서 무관: 5일째 다음 2일째 대출도 성공"
    L = LibraryLoan()
    eq(L.borrow("B001", "김", 5), True, "5일째")
    eq(L.borrow("B002", "김", 2), True, "2일째")
    eq(L.get_loans("김"), [("B002", 16), ("B001", 19)], "목록")


def t20():
    "빈 목록 · 실패한 대출은 기록 안 됨"
    L = LibraryLoan()
    eq(L.get_loans("아무도"), [], "모르는 사람")
    eq(L.borrow("B001", "김", 0), False, "실패한 대출")
    eq(L.get_loans("김"), [], "기록 없음")
    eq(L.borrow("B001", "이", 1), True, "B001은 비어 있음")
    L.return_book("B001", "이", 2)
    eq(L.get_loans("이"), [], "반납 후 빈 목록")


TESTS = [t01, t02, t03, t04, t05, t06, t07, t08, t09, t10,
         t11, t12, t13, t14, t15, t16, t17, t18, t19, t20]

if __name__ == "__main__":
    passed = 0
    for i, t in enumerate(TESTS, 1):
        try:
            t()
            passed += 1
            print(f"  [통과] {i:2}. {t.__doc__}")
        except AssertionError as e:
            print(f"  [실패] {i:2}. {t.__doc__}  ({e})")
        except Exception as e:
            print(f"  [에러] {i:2}. {t.__doc__}  ({type(e).__name__}: {e})")
    print(f"\n결과: {passed} / {len(TESTS)} 통과  (예상 점수 {passed * 4} / 80)")
