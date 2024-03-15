import unittest
from core.docx_template_placeholder import DocxTemplatePlaceholder
from constants.core_items import *

# константы вывести


class TestDOCXTemplatePlaceholder(unittest.TestCase):
    def test_standart_data_tags(self):
        data = dict()
        data[Process_items.KEYS] = {}
        data[Process_items.TABLES] = {}
        data[Process_items.KEYS]["hi"] = "Привет"
        data[Process_items.KEYS]["buy"] = "Покеда"
        data[Process_items.KEYS]["name"] = "Laplas"
        data[Process_items.KEYS]["lastname"] = "Solomon"
        data[Process_items.KEYS]['data'] = "February"
        data[Process_items.KEYS]['satana'] = 'God'
        data[Process_items.TABLES]['cryptocurrency_tb'] = [
            {
                "name": "Bitcoin",
                "symbol": "BTC",
                "price_usd": 39857.20,
                "price_eur": 34991.42,
                "price_gbp": 29489.55
            },
            {
                "name": "Ethereum",
                "symbol": "ETH",
                "price_usd": 2845.62,
                "price_eur": 2498.75,
                "price_gbp": 2104.89
            },
            {
                "name": "Ripple",
                "symbol": "XRP",
                "price_usd": 0.84,
                "price_eur": 0.74,
                "price_gbp": 0.62
            }]
        result = DocxTemplatePlaceholder("out_test_files",
                                "../test_files/test_file_keys.docx",
                                "test_file_keys_result_1",
                                data).process()
        expected_path = "../out_test_files/test_file_keys_result_1.pdf"
        self.assertEqual(result, expected_path)

    def test_only_keys_data_tags(self):
        data = {}
        data[Process_items.KEYS] = {}
        data[Process_items.KEYS]["hi"] = "Привет"
        data[Process_items.KEYS]["buy"] = "Покеда"
        data[Process_items.KEYS]["name"] = "Laplas"
        data[Process_items.KEYS]["lastname"] = "Solomon"
        data[Process_items.KEYS]['data'] = "February"
        data[Process_items.KEYS]['satana'] = 'God'
        result = DocxTemplatePlaceholder("out_test_files",
                                         "../test_files/test_file_keys.docx",
                                         "test_file_keys_result_2",
                                         data).process()
        expected_path = "../out_test_files/test_file_keys_result_2.pdf"
        self.assertEqual(result, expected_path)

    def test_only_tables_data_tags(self):
        data = {}
        data[Process_items.TABLES] = {}
        data[Process_items.TABLES]['cryptocurrency_tb'] = [
            {
                "name": "Bitcoin",
                "symbol": "BTC",
                "price_usd": 39857.20,
                "price_eur": 34991.42,
                "price_gbp": 29489.55
            },
            {
                "name": "Ethereum",
                "symbol": "ETH",
                "price_usd": 2845.62,
                "price_eur": 2498.75,
                "price_gbp": 2104.89
            },
            {
                "name": "Ripple",
                "symbol": "XRP",
                "price_usd": 0.84,
                "price_eur": 0.74,
                "price_gbp": 0.62
            }]
        result = DocxTemplatePlaceholder("out_test_files",
                                         "../test_files/test_file_keys.docx",
                                         "test_file_keys_result_3",
                                         data).process()
        expected_path = "../out_test_files/test_file_keys_result_3.pdf"
        self.assertEqual(result, expected_path)

    def test_empty_data_tags(self):
        data = {}
        result = DocxTemplatePlaceholder("out_test_files",
                                         "../test_files/test_file_keys.docx",
                                         "test_file_keys_result_4",
                                         data).process()
        expected_path = "../out_test_files/test_file_keys_result_4.pdf"
        self.assertEqual(result, expected_path)

    def test_some_tags_in_text(self):
        data = {}
        data[Process_items.KEYS] = {}
        data[Process_items.TABLES] = {}
        data[Process_items.KEYS]["hi"] = "Привет"
        data[Process_items.KEYS]["buy"] = "Покеда"
        data[Process_items.KEYS]["name"] = "Laplas"
        data[Process_items.KEYS]["lastname"] = "Solomon"
        data[Process_items.KEYS]['data'] = "February"
        data[Process_items.KEYS]['satana'] = 'God'
        data[Process_items.TABLES]['cryptocurrency_tb'] = [
            {
                "name": "Bitcoin",
                "symbol": "BTC",
                "price_usd": 39857.20,
                "price_eur": 34991.42,
                "price_gbp": 29489.55
            },
            {
                "name": "Ethereum",
                "symbol": "ETH",
                "price_usd": 2845.62,
                "price_eur": 2498.75,
                "price_gbp": 2104.89
            },
            {
                "name": "Ripple",
                "symbol": "XRP",
                "price_usd": 0.84,
                "price_eur": 0.74,
                "price_gbp": 0.62
            }]
        result = DocxTemplatePlaceholder("out_test_files",
                                         "../test_files/test_some_tags_in_text.docx",
                                         "test_some_tags_in_text",
                                         data).process()
        expected_path = "../out_test_files/test_some_tags_in_text"
        self.assertEqual(result, expected_path)

    def test_different_style_tags(self):
        data = {}
        data[Process_items.KEYS] = {}
        data[Process_items.TABLES] = {}
        data[Process_items.KEYS]["hi"] = "Привет"
        data[Process_items.KEYS]["buy"] = "Покеда"
        data[Process_items.KEYS]["name"] = "Laplas"
        data[Process_items.KEYS]["lastname"] = "Solomon"
        data[Process_items.KEYS]['data'] = "February"
        data[Process_items.KEYS]['satana'] = 'God'
        data[Process_items.TABLES]['cryptocurrency_tb'] = [
            {
                "name": "Bitcoin",
                "symbol": "BTC",
                "price_usd": 39857.20,
                "price_eur": 34991.42,
                "price_gbp": 29489.55
            },
            {
                "name": "Ethereum",
                "symbol": "ETH",
                "price_usd": 2845.62,
                "price_eur": 2498.75,
                "price_gbp": 2104.89
            },
            {
                "name": "Ripple",
                "symbol": "XRP",
                "price_usd": 0.84,
                "price_eur": 0.74,
                "price_gbp": 0.62
            }]
        result = DocxTemplatePlaceholder("out_test_files",
                                         "../test_files/test_table_in_text.docx",
                                         "test_table_in_text",
                                         data).process()
        expected_path = "../out_test_files/test_table_in_text.pdf"
        self.assertEqual(result, expected_path)

    def test_table_in_other_places(self):
        data = {}
        data[Process_items.KEYS] = {}
        data[Process_items.TABLES] = {}
        data[Process_items.KEYS]["hi"] = "Привет"
        data[Process_items.KEYS]["buy"] = "Покеда"
        data[Process_items.KEYS]["name"] = "Laplas"
        data[Process_items.KEYS]["lastname"] = "Solomon"
        data[Process_items.KEYS]['data'] = "February"
        data[Process_items.KEYS]['satana'] = 'God'
        data[Process_items.TABLES]['cryptocurrency_tb'] = [
            {
                "name": "Bitcoin",
                "symbol": "BTC",
                "price_usd": 39857.20,
                "price_eur": 34991.42,
                "price_gbp": 29489.55
            },
            {
                "name": "Ethereum",
                "symbol": "ETH",
                "price_usd": 2845.62,
                "price_eur": 2498.75,
                "price_gbp": 2104.89
            },
            {
                "name": "Ripple",
                "symbol": "XRP",
                "price_usd": 0.84,
                "price_eur": 0.74,
                "price_gbp": 0.62
            }]
        result = DocxTemplatePlaceholder("out_test_files",
                                         "../test_files/test_table_in_other_places.docx",
                                         "test_table_in_other_places",
                                         data).process()
        expected_path = "../out_test_files/test_table_in_other_places.pdf"
        self.assertEqual(result, expected_path)

    def test_near_tags(self):
        data = {}
        data[Process_items.KEYS] = {}
        data[Process_items.TABLES] = {}
        data[Process_items.KEYS]["hi"] = "Привет"
        data[Process_items.KEYS]["buy"] = "Покеда"
        data[Process_items.KEYS]["name"] = "Laplas"
        data[Process_items.KEYS]["lastname"] = "Solomon"
        data[Process_items.KEYS]['data'] = "February"
        data[Process_items.KEYS]['satana'] = 'God'
        data[Process_items.TABLES]['cryptocurrency_tb'] = [
            {
                "name": "Bitcoin",
                "symbol": "BTC",
                "price_usd": 39857.20,
                "price_eur": 34991.42,
                "price_gbp": 29489.55
            },
            {
                "name": "Ethereum",
                "symbol": "ETH",
                "price_usd": 2845.62,
                "price_eur": 2498.75,
                "price_gbp": 2104.89
            },
            {
                "name": "Ripple",
                "symbol": "XRP",
                "price_usd": 0.84,
                "price_eur": 0.74,
                "price_gbp": 0.62
            }]
        result = DocxTemplatePlaceholder("out_test_files",
                                         "../test_files/test_both_near_tags.docx",
                                         "test_both_near_tags",
                                         data).process()
        expected_path = "../out_test_files/test_both_near_tags.pdf"
        self.assertEqual(result, expected_path)

    def test_near_tables(self):
        data = {}
        data[Process_items.KEYS] = {}
        data[Process_items.TABLES] = {}
        data[Process_items.KEYS]["hi"] = "Привет"
        data[Process_items.KEYS]["buy"] = "Покеда"
        data[Process_items.KEYS]["name"] = "Laplas"
        data[Process_items.KEYS]["lastname"] = "Solomon"
        data[Process_items.KEYS]['data'] = "February"
        data[Process_items.KEYS]['satana'] = 'God'
        data[Process_items.TABLES]['cryptocurrency_tb'] = [
            {
                "name": "Bitcoin",
                "symbol": "BTC",
                "price_usd": 39857.20,
                "price_eur": 34991.42,
                "price_gbp": 29489.55
            },
            {
                "name": "Ethereum",
                "symbol": "ETH",
                "price_usd": 2845.62,
                "price_eur": 2498.75,
                "price_gbp": 2104.89
            },
            {
                "name": "Ripple",
                "symbol": "XRP",
                "price_usd": 0.84,
                "price_eur": 0.74,
                "price_gbp": 0.62
            }]
        result = DocxTemplatePlaceholder("out_test_files",
                                         "../test_files/test_near_tables.docx",
                                         "test_near_tables",
                                         data).process()
        expected_path = "../out_test_files/test_near_tables.pdf"
        self.assertEqual(result, expected_path)

    def test_tables_in_footer_header(self):
        data = dict()
        data[Process_items.KEYS] = {}
        data[Process_items.TABLES] = {}
        data[Process_items.KEYS]["hi"] = "Привет"
        data[Process_items.KEYS]["buy"] = "Покеда"
        data[Process_items.KEYS]["name"] = "Laplas"
        data[Process_items.KEYS]["lastname"] = "Solomon"
        data[Process_items.KEYS]['data'] = "February"
        data[Process_items.KEYS]['satana'] = 'God'
        data[Process_items.TABLES]['cryptocurrency_tb'] = [
            {
                "name": "Bitcoin",
                "symbol": "BTC",
                "price_usd": 39857.20,
                "price_eur": 34991.42,
                "price_gbp": 29489.55
            },
            {
                "name": "Ethereum",
                "symbol": "ETH",
                "price_usd": 2845.62,
                "price_eur": 2498.75,
                "price_gbp": 2104.89
            },
            {
                "name": "Ripple",
                "symbol": "XRP",
                "price_usd": 0.84,
                "price_eur": 0.74,
                "price_gbp": 0.62
            }]
        result = DocxTemplatePlaceholder("out_test_files",
                                         "../test_files/test_tables_in_footers_headers.docx",
                                         "test_tables_in_footers_headers",
                                         data).process()
        expected_path = "../out_test_files/test_tables_in_footers_headers.pdf"
        self.assertEqual(result, expected_path)

    def test_strange_text(self):
        data = dict()
        data[Process_items.KEYS] = {}
        data[Process_items.TABLES] = {}
        data[Process_items.KEYS]["hi"] = "Привет"
        data[Process_items.KEYS]["buy"] = "Покеда"
        data[Process_items.KEYS]["name"] = "Laplas"
        data[Process_items.KEYS]["lastname"] = "Solomon"
        data[Process_items.KEYS]['data'] = "February"
        data[Process_items.KEYS]['satana'] = 'God'
        data[Process_items.TABLES]['cryptocurrency_tb'] = [
            {
                "name": "Bitcoin",
                "symbol": "BTC",
                "price_usd": 39857.20,
                "price_eur": 34991.42,
                "price_gbp": 29489.55
            },
            {
                "name": "Ethereum",
                "symbol": "ETH",
                "price_usd": 2845.62,
                "price_eur": 2498.75,
                "price_gbp": 2104.89
            },
            {
                "name": "Ripple",
                "symbol": "XRP",
                "price_usd": 0.84,
                "price_eur": 0.74,
                "price_gbp": 0.62
            }]
        result = DocxTemplatePlaceholder("out_test_files",
                                         "../test_files/test_strange_text.docx",
                                         "test_strange_text",
                                         data).process()
        expected_path = "../out_test_files/test_strange_text.pdf"
        self.assertEqual(result, expected_path)
