#!/usr/bin/env python3


"""Tests harness for Netflix"""

# -------
# imports
# -------

from io import StringIO
from unittest import main, TestCase

from Netflix import netflix_solve, netflix_rmse, netflix_predict, get_actual, get_mov, get_cus


# -----------
# TestNetflix
# -----------


class TestNetflix(TestCase):

    """Test harness"""

    # ------------
    # netflix_rmse
    # ------------
    def test_rmse_1(self):
        """First RMSE test"""
        count = 1
        sum_sq_diff = 4
        self.assertEqual(netflix_rmse(count, sum_sq_diff), 2.00000)

    def test_rmse_2(self):
        """Second RMSE test"""
        count = 7
        sum_sq_diff = 17
        self.assertEqual(netflix_rmse(count, sum_sq_diff), 1.55839)

    def test_rmse_3(self):
        """Third RMSE test"""
        count = 8
        sum_sq_diff = 1
        self.assertEqual(netflix_rmse(count, sum_sq_diff), 0.35355)

    # ----------
    # get_actual
    # ----------
    def test_get_actual_1(self):
        """Fetch actual rating 3"""
        key_mov = "123"
        key_cus = "234"
        cache = {("123", "234"): 3}
        self.assertEqual(get_actual(key_mov, key_cus, cache), 3)

    def test_get_actual_2(self):
        """Check assert safety"""
        key_mov = "0"
        key_cus = "1417435"
        cache = {("1417435", "123"): 3}
        try:
            self.assertEqual(get_actual(key_mov, key_cus, cache), 0)
        except AssertionError:
            pass
        else:
            raise ValueError("Getter tried fetching non-positive integer")

    def test_get_actual_3(self):
        """Return 0 if not in cache"""
        key_mov = "999999999999"
        key_cus = "999999999999"
        cache = {("1417435", "123"): 3}
        self.assertEqual(get_actual(key_mov, key_cus, cache), 0)

    def test_get_actual_4(self):
        """Check assert safety"""
        key_cus = "0"
        key_mov = "2043"
        cache = {("1417435", "2043"): 3}
        try:
            self.assertEqual(get_actual(key_mov, key_cus, cache), 0)
        except AssertionError:
            pass
        else:
            raise ValueError("Getter tried fetching non-positive integer")

    # -------
    # get_mov
    # -------
    def test_get_mov_1(self):
        """Fetch movie avg for movie ID 2043"""
        key_mov = "2043"
        cache = {"2043": 3.77}
        self.assertEqual(get_mov(key_mov, cache), 3.77)

    def test_get_mov_2(self):
        """Return 0 if movie does not exist"""
        key_mov = "99999999"
        cache = {"2043": 3.77}
        self.assertEqual(get_mov(key_mov, cache), 0)

    def test_get_mov_3(self):
        """Another general test"""
        key_mov = "13"
        cache = {"13": 4.55}
        self.assertEqual(get_mov(key_mov, cache), 4.55)

    # -------
    # get_cus
    # -------
    def test_get_cus_1(self):
        """Fetch customer avg"""
        key_cus = "1417435"
        cache = {"1417435": 3.5}
        self.assertEqual(get_cus(key_cus, cache), 3.5)

    def test_get_cus_2(self):
        """Fetch 0 if customer does not exist"""
        key_cus = "99999999"
        cache = {"1417435": 3.5}
        self.assertEqual(get_cus(key_cus, cache), 0)

    def test_get_cus_3(self):
        """Fetch customer avg"""
        key_cus = "2312054"
        cache = {"2312054": 4.45}
        self.assertEqual(get_cus(key_cus, cache), 4.45)

    # ---------------
    # netflix_predict
    # ---------------
    def test_predict_1(self):
        """Our prediction based on movie and customer"""
        key_mov = "2043"
        key_cus = "1417435"
        mov_cache = {"2043": 3.77}
        cus_cache = {"1417435": 3.5}
        self.assertEqual(
            netflix_predict(key_mov, key_cus, mov_cache, cus_cache), 3.57)

    def test_predict_2(self):
        """Giving None movie and customer to force a return of 0"""
        key_mov = "999999999"
        key_cus = "999999999"
        mov_cache = {"2043": 3.77}
        cus_cache = {"1417435": 3.5}
        self.assertEqual(
            netflix_predict(key_mov, key_cus, mov_cache, cus_cache), 0)

    def test_predict_3(self):
        """Simply another test"""
        key_mov = "888"
        key_cus = "2312054"
        mov_cache = {"888": 3.77}
        cus_cache = {"2312054": 3.5}
        self.assertEqual(
            netflix_predict(key_mov, key_cus, mov_cache, cus_cache), 3.57)

    # -------------
    # netflix_solve
    # -------------
    def test_solve_1(self):
        """Example"""
        actual_cache = {("13", "615010"): 3.7, (
            "13", "1860468"): 3.7, ("13", "2131832"): 3.7}
        mov_cache = {"13": 3.7}
        cus_cache = {"615010": 3.7, "1860468": 3.7, "2131832": 3.7}

        str_in = StringIO(
            "13:\n615010\n1860468\n2131832\n")
        str_out = StringIO()
        netflix_solve(str_in, str_out, actual_cache, mov_cache, cus_cache)
        self.assertEqual(
            str_out.getvalue(), "13:\n3.7\n3.7\n3.7\nRMSE: 0.00")

    def test_solve_2(self):
        """Sample run throughs"""
        actual_cache = {("10", "952305"): 3.5, ("10", "1531863"):
                        3.2, ("1000", "2326571"): 3.9, ("1000", "977808"): 3.3}
        mov_cache = {"10": 4, "1000": 3.5}
        cus_cache = {"952305": 4, "1531863":
                     3.4, "2326571": 3.7, "977808": 3.3}

        str_in = StringIO("10:\n1952305\n1531863\n1000:\n2326571\n977808")
        str_out = StringIO()
        netflix_solve(str_in, str_out, actual_cache, mov_cache, cus_cache)
        self.assertEqual(
            str_out.getvalue(), "10:\n1.0\n3.7\n1000:\n3.5\n3.1\nRMSE: 0.60")

    def test_solve_3(self):
        """Test 3"""
        actual_cache = {("1", "30878"): 4, (
            "1", "2647871"): 3, ("1", "1283744"): 2}
        mov_cache = {"1": 3.6}
        cus_cache = {"30878": 5, "2647871": 4, "1283744": 3}

        str_in = StringIO("1:\n30878\n2647871\n1283744")
        str_out = StringIO()
        netflix_solve(str_in, str_out, actual_cache, mov_cache, cus_cache)
        self.assertEqual(
            str_out.getvalue(), "1:\n4.9\n3.9\n2.9\nRMSE: 0.90")


# ----
# main
# ----

if __name__ == "__main__":
    main()
