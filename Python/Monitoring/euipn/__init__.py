import os
import requests
from bs4 import BeautifulSoup
import datetime
import json
import re
import tqdm
import base64

class EUIPN():
    def __init__(self, username, password):
        """Initialize the class, create a session to access the url and login
        """
        self.url = 'https://www.tmdn.org/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
        }

        self.path = os.getcwd()
        self.session = requests.session()

        self._init_session()                                                                                                                            # initialize the session

        self._auth(username, password)

        self.monitoring_design_parser = {'ST13': lambda x: x,                                                                                           # The key is the api response key and the value is the parser function to the data
                                         'applicantName': lambda x: x[0].upper() if type(x) == list else x.upper(),
                                         'applicationDate': EUIPN._format_date,
                                         'applicationNumber': lambda x: x,
                                         'designNumber': lambda x: x,
                                         'designStatus': lambda x: x,
                                         'expiryDate': EUIPN._format_date,
                                         'imageUrls': lambda x: [self._download_image(img) for img in x],
                                         'indicationOfProduct': EUIPN._get_indication_of_product,
                                         'locarnoClass': lambda x: x,
                                         'office': lambda x: x,
                                         'preferredImageUrl': self._download_image,
                                         'publicationDate': EUIPN._format_date,
                                         'registrationDate': EUIPN._format_date,
                                         'representativeName': lambda x: x,
                                         'tProtection': lambda x: x,
                                         'thumbnailUrl': lambda x: x}

    @staticmethod
    def _check_request_response(request_response):
        """Check the request response, if the response is a bad response, status code different from 200 or there is any error messege throw an error.

        Args:
            request_response (requests obj): The response to the request.

        Raises:
            Exception: If the request response status code is different from 200.
            Exception: If there is any error message in the website.

        Returns:
            requests obj: the request response if there is no problem.
        """
        exceptions = ['https://www.tmdn.org/tmdsview-web/']                                                                                             # urls to check just the status code

        if request_response.status_code != 200:
            raise Exception(f'Bad request response: {request_response.status_code}')

        if request_response.url in exceptions:
            return request_response

        result = BeautifulSoup(request_response.text, 'html.parser').text                                                                               # parse the html page to search the message error
        if 'Please enable JavaScript to view the page content' in result:
            raise Exception('There are some issues with the amount of requests made to the url.'
                            'If there are any tabs in the browser with the website open, close them and wait for the website to respond correctly.')

        return request_response

    def _get_request(self, url, headers={}, parameters={}):
        """Make a request in the same session initialized using the GET method to the url.

        Args:
            url (str): The url to make the request.
            headers (dict, optional): The headers request. Defaults to {}.
            parameters (dict, optional): The query parameters to make the request. Defaults to {}.

        Returns:
            requests obj: The response to the request.
        """
        return  EUIPN._check_request_response(self.session.get(url, headers=headers, json=parameters))

    def _post_request(self, url, headers={}, parameters={}):
        """Make a request in the same session initialized using the POST method to the url.

        Args:
            url (str): The url to make the request.
            headers (dict, optional): The headers request. Defaults to {}.
            parameters (dict, optional): The query parameters to make the request. Defaults to {}.

        Returns:
            requests obj: The response to the request.
        """
        return  EUIPN._check_request_response(self.session.post(url, headers=headers, json=parameters))

    def _init_session(self):
        """Initialide the session the set the coockies
        """
        print('Session initialized')
        url = f'{self.url}tmdsview-web/'
        self._get_request(url, self.headers)

    @staticmethod
    def _base64_encoder(value):
        """Encode de value to base64.

        Args:
            value (str): The value to encode.

        Returns:
            str: The value encoded in base64.
        """
        return base64.b64encode(value.encode('utf-8')).decode('utf-8')                                                                                  # convert the value to byte-like, encode it in base64 and decode to utf-8

    def _add_items_to_headers(self, items):
        """Copy the default headers to make te requests and add news items to the dict, the self.headers should remain unchanged.

        Args:
            items (dict): A dict containg the items to add to the copied header

        Returns:
            dict: The headers with the parameters from the default headers and the items to make the requests.
        """
        new_header = self.headers.copy()
        new_header.update(items)
        return new_header

    def _auth(self, username, password):
        """Make the authentication to login as an user
        """
        print('Login / authentication')

        url = f'{self.url}ms-cgateway/login?'
        parameters = {'service': 'https://www.tmdn.org/network/my-network',
                      'username': EUIPN._base64_encoder(username),                                                                                      # to make the authentication the username and the password should be in base64
                      'password': EUIPN._base64_encoder(password)}

        headers = self._add_items_to_headers({'Content-Type': 'application/x-www-form-urlencoded'})
        self._post_request(url, headers, parameters)

    @staticmethod
    def get_dates():
        """Get the first day and the last day in the last month (@staticmethod)

        Returns:
            (str, str): The first day and the last day in the last month in the format YYYY-mm-dd
        """
        end_date = datetime.date.today().replace(day=1) - datetime.timedelta(days=1)                                                                    # get today date and replace the day to be the day 1, go back one day to get the last day of the last month
        start_date = end_date.replace(day=1)                                                                                                            # get the last month last day and replace the day to be the first day of the last month

        return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

    def get_query_parameters(self, file_path, replaces={}):
        """Read the json file in file_path and replace values that is in the replaces dict

        Args:
            path (str): The path to the json file that contain the query parameters.
            replaces (dict, optional): A dict containing the pattern to find in the json file as key and the value to replace as value. Defaults to {}.

        Returns:
            list: A list of dict containig the query parameters.
        """
        print(f'Reading json file: {os.path.basename(file_path)}')
        with open(file_path, 'r') as f:
            json_file = re.sub(r'\/\*\*.*\*\*\/', '', f.read(), flags= re.DOTALL)                                                                       # remove comments in the json file
            for pattern, replacement in replaces.items():
                json_file = re.sub(pattern, replacement, json_file)                                                                                     # replace the pattern to de value

        return json.loads(json_file)

    def _download_image(self, url):
        """Download in the memory an image given the url sorce.

        Args:
            url (str): The image sorce.

        Raises:
            Exception: If the image sorce could not be found

        Returns:
            byte: The image downloaded
        """

        return self._get_request(f'{url}.jpg' if '.jpg' not in url else url, headers=self.headers).content                                              # add the image file extension

    @staticmethod
    def _format_date(date_raw):
        """Format the date from 2021-07-12T12:00:00.000Z to 12/07/2021 (@staticmethod)

        Args:
            date_raw (str): A date in the format YYYY-mm-ddTHH:MM:SS.fffZ.

        Returns:
            str: The date in the format dd/mm/YYYY.
        """
        date = datetime.datetime.strptime(date_raw, '%Y-%m-%dT%H:%M:%S.%fZ').date()
        return date.strftime('%d/%m/%Y')

    @staticmethod
    def _get_indication_of_product(language_list):
        """get the indication of product in the english language.

        Args:
            language_list (list): A list of dict containing the product indication and the language.

        Returns:
            str: The product incication or None if its in the exception list
        """
        for language in language_list:
            if language['languageCode'] != 'en':
                continue

            product = language['indicationOfProduct'].upper()                                                                                           # get the product indication and break the loop
            break

        return product

    def _parse_design_data(self, data, columns):
        """Parse the data containing in the data dict and transform it in to a matrix

        Args:
            data (list): A list of dict containing the data to parse.
            columns (list): A list containing the columns to parse and return, the elements should match the columns returned from the API.

        Yields:
            list: A list of lists containing the parsed data.
        """
        print('Parsing data')
        for results in tqdm.tqdm(data, unit='rows'):
            yield [self.monitoring_design_parser[column](results[column]) if results.get(column) else '' for column in columns]                         # for each key in the self.data_parser, get the value in the row and parse it. The keys in the self.data_parser

    def get_design_data(self, query_parameters, columns):
        """Get the data from api given the query_parameters.

        Args:
            query_parameters (dict): A dict containing the search parameters
            columns (list): A list containing the columns to parse and return, the elements should match the columns returned from the API.

        Returns:
            list: A list of lists containing the data.
        """
        headers = self._add_items_to_headers({'Referer': f'{self.url}tmdsview-web/'})
        url = f'{self.url}tmdsview-web/api/search/dsv/results'

        result = []
        page = 1
        print('Fetch data:')
        while True:
            query_parameters['page'] = str(page)                                                                                                        # set the page to fetch the data, the api con fetch 200 row for each page
            result_raw = json.loads(self._post_request(url, headers, query_parameters).text)
            print(f'\tPage {page} of {result_raw["totalPages"]}')

            result.extend(result_raw['designResults'])                                                                                                  # if there is more than one page extend the data form the others

            if result_raw['totalPages'] > page:                                                                                                         # check it reached to the last page
                page += 1
                continue

            break                                                                                                                                       # break the loop if it has reached the last page

        return self._parse_design_data(result, columns)
