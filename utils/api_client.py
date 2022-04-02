from datetime import datetime
from typing import Dict, Any
import time
import math

import requests
from pydantic.class_validators import List

from config import config
from utils.cache import RedisCache


class APIClient:
    def get_answer_data(self, since: datetime, until: datetime) -> List[Dict[str, Any]]:
        """Retrieve answer data from API"""
        ret = []
        try:
            has_more = True
            current_page = 1
            while has_more:
                parameters = {
                    "site": config.STACK_EXCHANGE_SITE,
                    "fromdate": int(since.timestamp()),
                    "todate": int(until.timestamp()),
                    "access_token": config.STACK_EXCHANGE_TOKEN,
                    "key": config.STACK_EXCHANGE_KEY,
                    "page": current_page,
                    "sort": "votes"
                }
                resp = requests.get(
                    f"{config.STACK_EXCHANGE_HOST}/{config.STACK_EXCHANGE_ANSWERS_ENDPOINT}",
                    params=parameters,
                )
                resp.raise_for_status()
                resp_json = resp.json()

                ret += resp_json.get("items", [])

                has_more = resp_json.get("has_more", False)
                current_page += 1
                # wait to avoid throttling
                time.sleep(0.01)
        except Exception:
            return ret
        return ret

    def get_comment_data(self, answers: List[int]):
        """Retrieve comment data from API"""
        # split into chuncks because the api has upper limit
        ret = []
        cache = RedisCache()
        key = cache.generate_key("get_comment_data", answers)
        if cache.get_json(key):
            cache.get_json(key)
        for chuck in chunks(answers, 100):
            has_more = True
            current_page = 1
            while has_more:
                try:
                    parameters = {
                        "site": config.STACK_EXCHANGE_SITE,
                        "access_token": config.STACK_EXCHANGE_TOKEN,
                        "key": config.STACK_EXCHANGE_KEY,
                        "page": current_page,
                    }
                    resp = requests.get(
                        f"{config.STACK_EXCHANGE_HOST}/{config.STACK_EXCHANGE_ANSWERS_ENDPOINT}/{';'.join([str(item) for item in chuck])}/comments",
                        params=parameters,
                    )
                    resp.raise_for_status()
                    resp_json = resp.json()
                    ret += resp_json.get("items", [])
                    has_more = resp_json.get("has_more", False)
                    current_page += 1
                    time.sleep(0.01)
                except Exception as e:
                    return ret
        cache.store_json(key=key, value=ret)
        return ret

    def final_data(self, since: datetime, until: datetime):
        cache = RedisCache()
        key = cache.generate_key("final_data", [since, until])
        if cache.get_json(key):
            return cache.get_json(key)
        """Combine answer data and comment data to get the final response"""
        ret = {
            "total_accepted_answers": 0,
            "accepted_answers_average_score": 0,
            "average_answers_per_question": 0,
        }
        found_questions = set()
        total_accepted_score = 0
        answers = self.get_answer_data(since=since, until=until)
        for answer in answers:
            if answer.get("is_accepted"):
                ret["total_accepted_answers"] += 1
                total_accepted_score += answer["score"]
            found_questions.add(answer.get("question_id"))

        if found_questions:
            ret["average_answers_per_question"] = round(len(answers) / len(found_questions), 2)

        if ret["total_accepted_answers"]:
            ret["accepted_answers_average_score"] = (
                round(total_accepted_score / ret["total_accepted_answers"], 2)
            )

        top_ten_ids = [item["answer_id"] for item in answers[:10]]
        comments = self.get_comment_data(top_ten_ids)
        ret["top_ten_answers_comment_count"] = {
            answer_id: 0 for answer_id in top_ten_ids
        }
        for comment in comments:
            ret["top_ten_answers_comment_count"][comment["post_id"]] += 1
        cache.store_json(key=key, value=ret)
        return ret


def get_api_client() -> APIClient:
    """Get api client object"""

    return APIClient()


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]
