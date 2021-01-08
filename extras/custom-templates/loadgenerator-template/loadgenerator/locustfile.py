#!/usr/bin/python
#
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Exercises the frontend endpoints for the system
"""


import logging

from locust import HttpLocust, TaskSet, TaskSequence, task, seq_task, between

class AllTasks(TaskSequence):
    """
    wrapper for GroupedTasks sets
    """
    @seq_task(1)
    class UnconditionalTasks(TaskSet):
        """
        use UnconditionalTasks for Tasks run before any conditions must be met
        """
        @task(1)
        def example_unconditional_task(self):
            """
            insert task action
            """
            with self.client.get("/", catch_response=True) as response:
                for r_hist in response.history:
                    if r_hist.status_code > 200 and r_hist.status_code < 400:
                        response.failure("unconditional_task received redirect")
            logging.debug("unconditional_task complete")
            self.interrupt()
            
    @seq_task(2)
    class ConditionalTasks(TaskSet):
        """
        set of tasks to run after a condition is met
        add an additional class for each unique condition
        """
        @task(1)
        def example_conditional_task(self):
            """
            insert task action
            """
            with self.client.get("/", catch_response=True) as response:
                for r_hist in response.history:
                    if r_hist.status_code > 200 and r_hist.status_code < 400:
                        response.failure("conditional_task received redirect")
            logging.debug("conditional_task complete")
            self.interrupt()

class WebsiteUser(HttpLocust):
    """
    Locust class to simulate HTTP users
    """
    task_set = AllTasks
    wait_time = between(1, 1)
