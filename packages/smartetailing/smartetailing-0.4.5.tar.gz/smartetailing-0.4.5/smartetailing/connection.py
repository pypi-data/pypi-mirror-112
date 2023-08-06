import datetime
import logging
import re
from typing import List, Iterator, Dict, Tuple

import pyap
import requests
import urllib3.util
from bs4 import BeautifulSoup
from lxml import etree
from lxml.etree import Element

from smartetailing.objects import WebOrder, Order, AddressInfo, Item, Name


def set_customer_affiliate_shipping_method(my_order, text_dict):
    my_order.customer_id = my_order.customer_id or text_dict.get('Customer ID')
    my_order.shipping.method = my_order.shipping.method or text_dict.get('Shipping Method')
    my_order.affiliate_info.affiliate = my_order.affiliate_info.affiliate or text_dict.get('Affiliate')
    my_order.affiliate_info.commission = my_order.affiliate_info.commission or get_dollars(
        text_dict.get('Commission'))


def get_table(response: requests.Response) -> Tuple[BeautifulSoup, BeautifulSoup]:
    assert response.status_code == 200
    response_soup = BeautifulSoup(response.text, 'html.parser')
    return response_soup.find('table', attrs={'class': 'table'}), response_soup


def set_addresses(my_order, remainder_text):
    billing_address = get_address_information(remainder_text, "Billing Information")
    shipping_address = get_address_information(remainder_text, "Shipping Information")
    my_order.bill_address = billing_address or my_order.bill_address
    my_order.ship_address = shipping_address or my_order.ship_address


class SmartetailingConnection:
    def __init__(self, base_url: str = None, merchant_id: int = None, url_key: str = None,
                 web_url: str = None, username: str = None, password: str = None):
        self.base_url = base_url
        self.merchant_id = merchant_id
        self.url_key = url_key
        self.web_url = web_url
        self.username = username
        self.password = password

    def export_orders(self) -> List[Order]:
        """
        Export the order XML and generate the order objects
        :return:
        """
        try:
            order_xml = self.__export_order_xml()
            return [WebOrder().from_xml(order).order for order in order_xml.findall('WebOrder')]
        except ConnectionError as ce:
            # Try the web scraper?
            return self.export_orders_via_web()

    def confirm_order_receipts(self, order_ids: Iterator[str]) -> None:
        for order_id in order_ids:
            self.__update_order(order_id)
            logging.info(f"Updated order {order_id}")

    def update_order_status(self, order_id: str, order_status: str) -> None:
        self.__update_status(order_id, order_status)
        logging.info(f"Updated order={order_id} to status={order_status}")

    def export_orders_via_web(self) -> List[Order]:
        my_session, order_information = self.__get_open_orders(self.__login())
        my_session.close()
        return order_information

    def __parse_html(self, html_data: Element) -> List[WebOrder]:
        raise NotImplementedError

    def __login(self) -> requests.Session:
        s = requests.Session()
        login_page = s.get(self.web_url + "/login.cfm", params={"CFTOKEN": 0, "cookie": "yes"})
        assert login_page.status_code == 200

        login_response = s.post(self.web_url + "/continue.cfm", data={
            "Domain": urllib3.util.parse_url(self.web_url).host,
            "Login": self.username,
            "Pass": self.password
        }, allow_redirects=True)
        assert login_response.status_code == 200
        index_response = s.get(self.web_url + "/index.cfm")
        assert index_response.status_code == 200

        return s

    def __get_open_orders(self, s: requests.Session) -> Tuple[requests.Session, List[Order]]:
        open_orders_response = s.get(self.web_url + "/orders/openorders.cfm", params={
            "Status": 2,
            "startYear": 1900,
            "sort": "Created",
            "ordertype": "desc"
        })
        table_tag, open_orders_soup = get_table(open_orders_response)

        # Get the order id's
        order_ids = [input_tag['value'] for input_tag in table_tag.find_all('input', attrs={'type': 'Checkbox'})]
        order_ids = [order_id for order_id in order_ids if order_id != '1']

        # Open each order
        all_orders = list()
        for order_id in order_ids:
            order_detail_response = s.get(f"{self.web_url}/orders/vieworder.cfm", params={'ID': order_id})
            order_detail_table, order_detail_soup = get_table(order_detail_response)

            my_order = Order()

            order_heading_tag = order_detail_soup.find('div', attrs={'class': 'panel-heading seaorderheading'})
            order_number_time_text = order_heading_tag.text.strip()
            z = re.match(r"Order: (\d+-\d+-\d+)Created: (\d+-\d+-\d+), (\d+:\d+)", order_number_time_text)
            if z:
                my_order.id = z.group(1)
                my_order.time = datetime.datetime.strptime(f"{z.group(2)} {z.group(3)}", "%m-%d-%Y %H:%M")

            for table_row in order_detail_table.find_all('tr', recursive=False):
                for table_item in table_row.find_all('td', recursive=False):
                    text_lines = [line for line in table_item.text.split('\n') if line]
                    text_dict, remainder_text = text_to_dictionary(text_lines)

                    set_addresses(my_order, remainder_text)
                    set_customer_affiliate_shipping_method(my_order, text_dict)
                    set_order_total(my_order, text_dict)

                    my_order.comments = text_dict.get('Additional Info')
                    end_index = 0
                    for index, item in enumerate(text_lines):
                        # We are in the middle of an item block, just skip the rest.
                        if index < end_index:
                            continue
                        item_number_match = re.search(r"My #:(\d+)", item)
                        qbp_number_match = re.search(r"[A-Z]+ #:([\w\d\-]+)", item)
                        if item_number_match or qbp_number_match:
                            item_number = item_number_match.group(1) if item_number_match else qbp_number_match.group(1)
                            end_index = self.add_item_to_order(item_number, index, my_order, text_lines)
            # Get order status
            order_status_table = order_detail_soup.find('table', attrs={'class': 'table form-inline'})
            order_status = order_status_table.find('option', attrs={'selected': ''})
            my_order.status = order_status.text
            all_orders.append(my_order)
            logging.info(f'Order #{order_id} scraped')

        return s, all_orders

    def add_item_to_order(self, item_number, item_number_index, my_order, text_lines) -> int:
        my_item = Item()
        my_item.id = item_number
        my_item.mpn = item_number
        # my_item.gtin1 = qbp_number
        # Locate the item name
        try:
            start_index = text_lines.index('More', item_number_index)
        except ValueError:
            start_index = item_number_index
        end_index = text_lines.index("Add Note", start_index)
        my_item.description = "\n".join(text_lines[start_index + 1:end_index - 2])
        my_order.items.append(my_item)
        return end_index

    def __export_order_xml(self) -> Element:
        r = self.__make_http_request(self.base_url, 'Orders', self.merchant_id, self.url_key)
        return etree.XML(r.content)

    def __update_order(self, order_id: str) -> requests.Response:
        return self.__make_http_request(self.base_url, 'UpdateOrder', self.merchant_id, self.url_key, order_id)

    def __update_status(self, order_id: str, order_status: str) -> requests.Response:
        return self.__make_http_request(self.base_url, 'UpdateStatus', self.merchant_id, self.url_key, order_id,
                                        order_status)

    @staticmethod
    def __make_http_request(base_url: str, method: str, merchant_id: int, url_key: str, order_id: str = '',
                            order_status: str = '') -> requests.Response:
        query_parameters: dict = {
            'method': method,
            'ver': '2.00',
            'merchant': f'{merchant_id}',
            'URLkey': url_key,
            'OrderNumber': order_id,
            'OrderStatus': order_status
        }
        r = requests.get(base_url, params=query_parameters)
        SmartetailingConnection.__handle_http_error(r)
        return r

    @staticmethod
    def __handle_http_error(response: requests.Response) -> None:
        if response.status_code == 503:
            raise ConnectionError(f"Error {response}")
        if response.status_code >= 300:
            logging.debug(response)
            raise RuntimeError(f"Error {response}")


def text_to_dictionary(text_lines: List[str]) -> Tuple[Dict[str, str], List[str]]:
    text_dict = dict()
    remainder_text = list()
    ij = 0
    while ij < len(text_lines):
        if text_lines[ij].endswith(":"):
            key = text_lines[ij]
            has_value = ij + 1 < len(text_lines) and not text_lines[ij + 1].endswith(":")
            value = text_lines[ij + 1] if has_value else ""
            text_dict[key.rstrip(':')] = value
            if has_value:
                # Skip the value to prevent copying into remainder list
                ij += 1
        else:
            remainder_text.append(text_lines[ij])
        ij += 1
    return text_dict, remainder_text


def get_address_information(text_lines: List[str], information_key) -> AddressInfo:
    try:
        index = text_lines.index(information_key)
        text = "\n".join([l.strip() for l in text_lines])
        addresses = pyap.parse(text, country="us")
        if addresses:
            address = addresses[0].as_dict()
        elif len(text_lines) >= 9:
            us_index = text_lines.index('United States')
            address = {'full_street': text_lines[index+2].strip(','),
                       'city': text_lines[us_index-3].strip(','),
                       'region1': text_lines[us_index-2].strip(','),
                       'postal_code': text_lines[us_index-1].strip(','),
                       'country_id': text_lines[us_index].strip(',')}
            if index+2 < us_index-4:
                address['address_2'] = text_lines[us_index-4]
        else:
            address = {}
        my_address = AddressInfo()
        my_address.name = Name(text_lines[index + 1])
        my_address.email = get_email_address(text_lines)
        my_address.phone = get_phone_number(text_lines)
        my_address.address1 = address.get('full_street', '')
        my_address.address2 = address.get('address_2', '')
        my_address.city = address.get('city', '')
        my_address.zip = address.get('postal_code', '')
        my_address.state = address.get('region1', '')
        my_address.country = address.get('country_id', '')
        return my_address
    except ValueError:
        return None
    except IndexError:
        return None


__EMAIL_REGEX__ = r"[a-z0-9.\-+_]+@[a-z0-9.\-+_]+\.[a-z]+"
__PHONE_REGEX__ = r"\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*"


def get_email_address(text_lines: List[str]) -> str:
    text = "\n".join([l.strip() for l in text_lines])
    emails: List[str] = re.findall(__EMAIL_REGEX__, text)
    if emails:
        return emails[0]
    else:
        return ''


def get_phone_number(text_lines: List[str]) -> str:
    text = "\n".join(text_lines)
    phones: List[str] = re.findall(__PHONE_REGEX__, text)
    if phones:
        phone = [s for s in phones[0] if s]
        if len(phone) == 4:
            return f"+{'-'.join(phone)}"
        elif len(phone) == 3:
            return f"+1-{'-'.join(phone)}"
        else:
            raise ValueError("Could not format phone number")
    else:
        return ''


def set_order_total(my_order, text_dict):
    my_order.order_total.tax = my_order.order_total.tax or get_dollars(text_dict.get('Sales Tax'))
    my_order.order_total.shipping = my_order.order_total.shipping or get_dollars(
        text_dict.get('Shipping & Handling'))
    my_order.order_total.subtotal = my_order.order_total.subtotal or get_dollars(
        text_dict.get('Subtotal'))
    my_order.order_total.total = my_order.order_total.total or get_dollars(text_dict.get('GRAND TOTAL'))
    my_order.order_total.discount = my_order.order_total.discount or get_dollars(
        text_dict.get('Total Discount'))


def get_dollars(text: str) -> float:
    return float("0" + (text or "0").replace(",", "").strip("$"))
