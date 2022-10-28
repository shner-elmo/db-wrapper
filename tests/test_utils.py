import unittest
import sqlite3

from pandasdb.utils import *

DB_FILE = '../data/forestation.db'
SQL_FILE = '../data/parch-and-posey.sql'
SQLITE_FILE = '../data/mental_health.sqlite'


class TestUtils(unittest.TestCase):
    def test_convert_type_to_sql(self):
        self.assertEqual(convert_type_to_sql('jake snake'), "'jake snake'")
        self.assertEqual(convert_type_to_sql(394), '394')
        self.assertEqual(convert_type_to_sql(42.43), '42.43')
        self.assertEqual(convert_type_to_sql(True), 'true')
        self.assertEqual(convert_type_to_sql(False), 'false')

    def test_sql_tuple(self):
        out = sql_tuple(('jake', 32.2, True, 'new york'))
        self.assertEqual(out, "('jake', 32.2, true, 'new york')")

        out = sql_tuple((False,))
        self.assertEqual(out, '(false)')

    def test_sqlite_conn_open(self):
        conn = sqlite3.connect(DB_FILE)
        # with conn as cur:
        #     cur.execute('SELECT ')
        conn.cursor()  # if connection is closed it will raise an error when asked for a cursor
        self.assertIs(sqlite_conn_open(conn), True)
        conn.close()
        self.assertIs(sqlite_conn_open(conn), False)

        self.assertRaises(sqlite3.ProgrammingError, conn.cursor)

    def test_get_random_name(self):
        out = get_random_name(5)
        self.assertIsInstance(out, str)
        self.assertTrue(out.islower())
        self.assertEqual(len(out), 5)

        # assert set doesn't shrink in size (all elements unique)
        random_names = {
            get_random_name(), get_random_name(),
            get_random_name(), get_random_name(),
            get_random_name(), get_random_name()
        }
        self.assertEqual(len(random_names), 6)

    def test_create_view(self):
        conn = sqlite3.connect(DB_FILE)
        name = f'test_view_{get_random_name()}'
        query = 'SELECT * FROM forest_area LIMIT 50'
        create_view(conn=conn, view_name=name, query=query, drop_if_exists=True)

        with conn as cur:
            view_data: list[tuple[Any]] = cur.execute(f'SELECT * FROM {name}').fetchall()
            table_data: list[tuple[Any]] = cur.execute(query).fetchall()
        self.assertEqual(view_data, table_data)

        self.assertRaisesRegex(
            ValueError,
            f"view '{name}' already exists",
            create_view, conn=conn, view_name=name, query=query, drop_if_exists=False
        )
        # TODO complete test

    def test_same_val_generator(self):
        val = random.random()
        size = 9

        it = same_val_generator(val=val, size=size)
        for x in it:
            self.assertEqual(x, val)

        it = same_val_generator(val=val, size=size)
        self.assertEqual(len(tuple(it)), size)

    def test_infinite_generator(self):
        val = random.random()
        it = infinite_generator(val=val)
        
        for x, _ in zip(it, range(100)):
            self.assertEqual(x, val)

    def test_concat(self):
        pass

    def test_mb_size(self):
        pass

    def test_rename_duplicate_cols(self):
        pass

    def test_convert_db_to_sql(self):
        pass

    def test_convert_csvs_to_db(self):
        pass

    def test_convert_sql_to_db(self):
        pass

    def test_load_sql_to_sqlite(self):
        pass


if __name__ == '__main__':
    unittest.main()
