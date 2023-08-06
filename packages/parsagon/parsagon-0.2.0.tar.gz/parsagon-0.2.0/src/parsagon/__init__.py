import asyncio
import json
import datetime
import time

from progress.bar import Bar
import requests

try:
    import parsagon_local_drivers
except ImportError:
    parsagon_local_drivers = None


TIMEOUT=300
ENVIRONMENTS = {
    'local': 'LOCAL',
    'cloud': 'DC',
    'unblockable': 'RESID',
}
SCROLL_SPEEDS = {
    'fast': 'FAST',
    'medium': 'MEDIUM',
    'slow': 'SLOW',
}
FORMATS = {
    'json': 'json_format',
    'csv': 'csv_format',
}
OUTPUTS = set(['data', 'file'])
STARTING_LIMIT = 64
MAX_RESPONSE_THRESHOLD = 2 ** 20


class ScraperRunError(Exception):
    def __init__(self, message, checkpoint):
        super().__init__(message)
        self.checkpoint = checkpoint


class Client:
    def __init__(self, username, password, host='parsagon.io'):
        data = {'username': username, 'password': password}
        r = requests.post(f'https://{host}/api/accounts/token-auth/', json=data, timeout=TIMEOUT)
        if not r.ok:
            self._display_errors(r)
        self.token = r.json()['token']
        self.host = host

    def _display_errors(self, response):
        if response.status_code == 500:
            raise Exception('A server error occurred. Please notify Parsagon.')
        if response.status_code in (502, 503, 504):
            raise Exception('Lost connection to server. To try again later, rerun execute() with retry=True')
        errors = response.json()
        if 'non_field_errors' in errors:
            raise Exception(errors['non_field_errors'])
        else:
            raise Exception(errors)

    def _get_result(self, result_id, format, output, file_path, urls):
        headers = {'Content-Type': 'application/json', 'Authorization': f'Token {self.token}'}
        r = requests.post(f'https://{self.host}/api/scrapers/results/{result_id}/execute/', headers=headers, timeout=TIMEOUT)
        if not r.ok:
            self._display_errors(r)
        bar = Bar('Collecting data', max=len(urls), suffix='%(percent)d%%')
        num_scraped = 0
        while True:
            r = requests.get(f'https://{self.host}/api/scrapers/results/{result_id}/progress/', headers=headers, timeout=TIMEOUT)
            if not r.ok:
                self._display_errors(r)
            result_data = r.json()
            if result_data['status'] == 'FINISHED':
                for i in range(len(urls) - num_scraped):
                    bar.next()
                bar.finish()
                break
            elif result_data['status'] == 'ERROR':
                bar.finish()
                raise ScraperRunError('A server error occurred. Please notify Parsagon.', result_data['checkpoint'])
            elif 'num_scraped' in result_data and result_data['num_scraped'] > num_scraped:
                for i in range(result_data['num_scraped'] - num_scraped):
                    bar.next()
                num_scraped = result_data['num_scraped']

            time.sleep(5)

        print('Downloading data...')
        if output == 'file':
            with open(file_path, 'w') as f:
                if format == 'csv':
                    raise Exception("Output type 'file' not yet supported for format 'csv'")
                else:
                    offset = 0
                    limit = STARTING_LIMIT
                    offset_incr = 0
                    max_response_size = 0
                    r = requests.get(f'https://{self.host}/api/scrapers/results/{result_id}/download/?data_format={format}&offset={offset}&limit={limit}', headers=headers, timeout=TIMEOUT)
                    if not r.ok:
                        self._display_errors(r)
                    result_data = r.json()
                    offset_incr = len(result_data['result'])
                    offset += offset_incr
                    new_data = json.dumps(result_data)
                    f.write(new_data[:-2])
                    max_response_size = max(max_response_size, len(new_data))

                    while offset_incr == limit:
                        if max_response_size < MAX_RESPONSE_THRESHOLD:
                            limit *= 2

                        r = requests.get(f'https://{self.host}/api/scrapers/results/{result_id}/download/?data_format={format}&offset={offset}&limit={limit}', headers=headers, timeout=TIMEOUT)
                        if r.status_code == 504:
                            if limit == 1:
                                raise Exception('Data download timed out')
                            limit //= 2
                            offset_incr = limit
                            max_response_size = MAX_RESPONSE_THRESHOLD
                            continue
                        if not r.ok:
                            self._display_errors(r)
                        result_data = r.json()
                        offset_incr = len(result_data['result'])
                        if not offset_incr:
                            break
                        offset += offset_incr
                        new_data = json.dumps(result_data['result'])
                        new_data = ',' + new_data[1: -1]
                        f.write(new_data)
                        max_response_size = max(max_response_size, len(new_data))
                    f.write('}}')
        else:
            r = requests.get(f'https://{self.host}/api/scrapers/results/{result_id}/download/?data_format={format}',
                             headers=headers, timeout=TIMEOUT)
            if not r.ok:
                self._display_errors(r)
            data = r.json()
            if format == 'csv':
                return data['result']
            else:
                return data

    def execute(self, scraper_name, urls, env, max_page_loads=1, scroll_speed='fast', action_settings={}, format='json', output='data', file_path='', is_retry=False):
        if env not in ENVIRONMENTS:
            raise ValueError("Environment must be 'local', 'cloud', or 'unblockable'")
        if env == 'local' and not parsagon_local_drivers:
            raise ValueError("Cannot use local environment without local drivers. Install parsagon-local-drivers to continue.")
        if scroll_speed not in SCROLL_SPEEDS:
            raise ValueError("Scroll speed must be 'fast', 'medium', or 'slow'")
        if format not in FORMATS:
            raise ValueError("Format must be 'json' or 'csv'")
        if output not in OUTPUTS:
            raise ValueError("Output must be 'data' or 'file'")
        if output == 'file' and not file_path:
            raise ValueError("Output type is 'file' but no file path was given")

        headers = {'Content-Type': 'application/json', 'Authorization': f'Token {self.token}'}

        data = {'scraper_name': scraper_name, 'urls': urls, 'max_page_loads': max_page_loads, 'scroll_speed': SCROLL_SPEEDS[scroll_speed], 'action_settings': action_settings, 'environment': ENVIRONMENTS[env], 'is_retry': is_retry}
        r = requests.post(f'https://{self.host}/api/scrapers/results/find-redundant/', headers=headers, json=data, timeout=TIMEOUT)
        if not r.ok:
            self._display_errors(r)
        result = r.json()

        if not result.get('id2'):
            data = {'scraper_name': scraper_name, 'urls': urls, 'max_page_loads': max_page_loads, 'scroll_speed': SCROLL_SPEEDS[scroll_speed], 'action_settings': action_settings}
            r = requests.post(f'https://{self.host}/api/scrapers/runs/', headers=headers, json=data, timeout=TIMEOUT)
            if not r.ok:
                self._display_errors(r)
            run = r.json()

            if not run['scraper'][FORMATS[format]]:
                raise Exception(f'{format} format is unavailable for this scraper')

            data = {'environment': ENVIRONMENTS[env]}
            r = requests.post(f'https://{self.host}/api/scrapers/runs/{run["id2"]}/results/', headers=headers, json=data, timeout=TIMEOUT)
            if not r.ok:
                self._display_errors(r)
            result = r.json()
        elif not result['scraper'][FORMATS[format]]:
            raise Exception(f'{format} format is unavailable for this scraper')

        if env == 'local':
            driver = parsagon_local_drivers.Chrome(result['id2'], self.host)

        checkpoint = result['checkpoint']
        while True:
            try:
                return_value = self._get_result(result['id2'], format, output, file_path, urls)
                break
            except ScraperRunError as e:
                if checkpoint == e.checkpoint:
                    if env == 'local':
                        driver.quit()
                    raise e
                else:
                    checkpoint = e.checkpoint

        if env == 'local':
            driver.quit()

        return return_value
