# Copyright (C) 2021 Spiralworks Technologies Inc.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN

import logging
import os
import hashlib
import shutil
import time
import json
import pandas as pd
import asyncio
import glob

from pyppeteer import launch
from subprocess import Popen, STDOUT

from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

from LighthouseLibrary.version import VERSION


LOGGER = logging.getLogger(__name__)
DEFAULT_TAG = 'default'

BATCH_COMMAND = "lighthouse-batch"
PARALLEL_COMMAND = "lighthouse-batch-parallel"
INPUT_FILE = "input.csv"


def absolute_path(file):
    if file.startswith('/'):
        return file
    else:
        return os.path.join(os.getcwd(), file)


async def screenshot(file: str, requested_url, output_file):
    browser = await launch(headless=True)
    page = await browser.newPage()

    await page.goto(f'file:{absolute_path(file)}')
    script = '''() => {
        var el = document.querySelector('.lh-topbar__url');
        el.setAttribute('href', 'REQUESTED_URL');
        el.setAttribute('title', 'REQUESTED_URL');
        el.innerHTML = 'REQUESTED_URL'
        return 1
    }'''

    await page.evaluate(script.replace('REQUESTED_URL', requested_url))
    await page.screenshot({
        'path': absolute_path(output_file),
        'fullPage': True
    })
    await browser.close()


class LighthouseLibrary:

    def _create_command(self, command, file, args: list):
        return [command, *args, "-f", file]

    def _create_base_dir(self):
        target_dir = "target"
        os.makedirs(target_dir, exist_ok=True)

        output_dir = os.path.join(target_dir, "lighthouse")
        shutil.rmtree(output_dir, ignore_errors=True)
        os.makedirs(output_dir, exist_ok=True)

        return output_dir

    def _create_csv(self, file, urls: list):
        data = {"url": urls}
        df = pd.DataFrame(data=data, columns=["url"])
        df.to_csv(file, header=False, index=False)

    def _process_html_file(self, html_file):
        base_file = html_file[:len(html_file) - 5]
        json_file = f'{base_file}.json'
        output_file = f'{base_file}.png'

        with open(json_file, 'r') as f:
            json_data = json.load(f)
            requested_url = json_data['requestedUrl']
            asyncio.get_event_loop().run_until_complete(screenshot(html_file, requested_url, output_file))

        return output_file

    def _generate_image_reports(self, lighthouse_dir):
        output_files = []
        for html_file in glob.glob(os.path.join(lighthouse_dir, '*.html')):
            output_files.append(self._process_html_file(html_file))

        return output_files

    def batch(self, config):
        assert 'urls' in config, 'No urls found'

        start = time.time()
        base_dir = self._create_base_dir()

        # create the csv file based from the config
        csv_file = os.path.join(base_dir, INPUT_FILE)
        self._create_csv(csv_file, config['urls'])

        args = []
        if config.get('print', True):
            args.append("--print")
        if config.get('verbose', False):
            args.append("-v")
        if config.get('html', True):
            args.append("-h")

        addition_args = config.get('args', [])
        args.extend(addition_args)

        command_list = self._create_command(BATCH_COMMAND, INPUT_FILE, args)
        summary = []
        command = [f"cd {base_dir}", " ".join(command_list)]
        commands = "; ".join(command)
        LOGGER.info(f'command: {commands}')
        return_code = os.system(commands)
        LOGGER.info(f"return code: {return_code}")
        lighthouse_dir = f'{base_dir}/report/lighthouse'
        with open(os.path.join(lighthouse_dir, 'summary.json'), 'r') as f:
            summary = json.load(f)

        if config.get('image', True):
            self._generate_image_reports(lighthouse_dir)

            for item in summary:
                item['image'] = f'{item["name"]}.report.png'

        LOGGER.info(f"Completed in ({time.time() - start}s)")

        return summary
