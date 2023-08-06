# -*- coding: utf-8 -*-
import logging

import allure

logging.basicConfig(level=logging.INFO)
Logger = logging.getLogger()


def log(name, body=None):
    allure.attach(name=str(name), body=str(body), attachment_type=allure.attachment_type.TEXT)
    msg = name if len(str(body)) > 100 or body is None else f"{name}:{body}"
    Logger.info(msg)
    return True


def step(title):
    title = f"Step:{title}"
    Logger.info(title)
    return allure.step(title)


def story(*stories):
    """установка меток testcase и story"""
    def inner(func):
        allure.story(*stories)(func)
        allure.testcase(f"http://testrail.vsk.ru/index.php?/cases/view/{stories[0]}", stories[0])(func)
        return func
    return inner
    # return allure.story(*stories)
