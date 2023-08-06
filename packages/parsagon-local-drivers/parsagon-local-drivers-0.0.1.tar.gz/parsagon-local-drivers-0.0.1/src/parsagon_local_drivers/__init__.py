import asyncio
import threading
import time
import json
from selenium import webdriver
from selenium.common.exceptions import JavascriptException, NoSuchElementException
from selenium.webdriver import ActionChains
import chromedriver_binary
import websockets


class Chrome:
    def __init__(self, result_id, host):
        self.result_id = result_id
        self.host = host

        self.exit_event = threading.Event()
        driver_task = threading.Thread(target=self._run_driver)
        driver_task.start()
        time.sleep(5)

    def quit(self):
        self.exit_event.set()
        time.sleep(3)

    def _run_driver(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._handle_driver())
        loop.close()

    async def _handle_driver(self):
        driver = webdriver.Chrome()
        async with websockets.connect(f'wss://{self.host}/ws/scrapers/results/{self.result_id}/client/') as websocket:
            while not self.exit_event.is_set():
                try:
                    message_str = await asyncio.wait_for(websocket.recv(), timeout=2)
                except asyncio.TimeoutError:
                    continue
                message = json.loads(message_str)
                convo_id = message['convo_id']
                response = 'OK'
                command = message['command']
                if command == 'get':
                    driver.get(message['url'])
                    await asyncio.sleep(2)
                elif command == 'mark':
                    elem_idx = driver.execute_script(f"let elemIdx = {message['elem_idx']}; for (const node of document.querySelectorAll(':not([data-parsagon-io-marked])')) {{ node.setAttribute('data-parsagon-io-marked', elemIdx); elemIdx++; }} return elemIdx;")
                    await websocket.send(json.dumps({'response': elem_idx, 'convo_id': convo_id}))
                    continue
                elif command == 'scroll':
                    await self._scroll(driver, message['speed'])
                elif command == 'click':
                    actions = ActionChains(driver)
                    target = driver.find_element_by_xpath(f"//*[@data-parsagon-io-marked={message['target_id']}]")
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});", target)
                    await asyncio.sleep(0.5)
                    try:
                        if message.get('human-like', True):
                            actions.move_to_element(target).click().perform()
                        else:
                            driver.execute_script("arguments[0].click();", target)
                        await asyncio.sleep(2)
                        await self._scroll(driver, message['speed'])
                    except JavascriptException:
                        pass
                elif command == 'inspect':
                    query = message['query']
                    if query == 'url':
                        response = driver.current_url
                    elif query == 'page_source':
                        response = driver.page_source
                    elif query == 'target_data':
                        try:
                            target = driver.find_element_by_xpath(f"//*[@data-parsagon-io-marked={message['target_id']}]")
                            tag = target.tag_name
                            text = target.text
                            href = target.get_attribute('href')
                            url = driver.execute_script(f"return document.querySelector('[data-parsagon-io-marked=\"{message['target_id']}\"]').href;")
                            response = {'tag': tag, 'text': text, 'href': href, 'url': url}
                        except NoSuchElementException:
                            response = {'tag': None}
                await websocket.send(json.dumps({'response': response, 'convo_id': convo_id}))
        driver.quit()

    async def _scroll(self, driver, speed):
        if speed == 'FAST':
            driver.execute_script("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});")
            await asyncio.sleep(1)
        elif speed == 'MEDIUM':
            position = driver.execute_script("return window.pageYOffset;")
            page_height = driver.execute_script("return document.body.scrollHeight;")
            for i in range(1, 6):
                new_position = position + (page_height - position) * i / 5
                driver.execute_script(f"window.scrollTo({{top: {new_position}, behavior: 'smooth'}});")
                await asyncio.sleep(0.5)
                new_elems = driver.execute_script("return document.querySelectorAll(':not([data-parsagon-io-marked])').length;")
                if new_elems:
                    break
            await asyncio.sleep(0.5)
        elif speed == 'SLOW':
            position = driver.execute_script("return window.pageYOffset;")
            page_height = driver.execute_script("return document.body.scrollHeight;")
            for i in range(1, 11):
                new_position = position + (page_height - position) * i / 10
                driver.execute_script(f"window.scrollTo({{top: {new_position}, behavior: 'smooth'}});")
                await asyncio.sleep(1)
                new_elems = driver.execute_script("return document.querySelectorAll(':not([data-parsagon-io-marked])').length;")
                if new_elems:
                    break
            await asyncio.sleep(1)
