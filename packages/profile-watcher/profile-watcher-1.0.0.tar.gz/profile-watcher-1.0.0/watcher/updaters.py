#!/usr/bin/python
# A python library that provides update when
# something changes in social profiles.
# Copyright (C) 2021 Shubhendra Kushwaha
# @TheShubhendra shubhendrakushwaha94@gmail.com
# This file is a part of profile-watcher <https://github.com/TheShubhendra/profile-watcher>.
#
# profile-watcher is a free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# profile-watcher is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with profile-watcher.  If not, see <http://www.gnu.org/licenses/>.


import asyncio
import logging
from quora import User
from quora.exceptions import ProfileNotFoundError
from .events.quora import (
    FollowingCountChange,
    FollowerCountChange,
    AnswerCountChange,
)


class Quora:
    def __init__(
        self,
        username,
        watcher,
        current_state=None,
        stateIntializer=None,
        update_interval=10,
        session=None,
    ):
        self.state = current_state
        self.user = User(username, session=session)
        self.watcher = watcher
        self.stateIntializer = stateIntializer
        self.logger = logging.getLogger(__name__)
        self.update_interval = update_interval

    async def check(self):
        try:
            await self.user.profile()
        except ProfileNotFoundError as e:
            print(e, self.user.username)
            return False
        return True

    async def _update(self):
        self.logger.debug(f"Updating quora profile of {self.user.username}")
        profile = await self.user.profile()
        if self.state is None:
            if self.stateIntializer is not None:
                profile = self.stateIntializer(profile)
            self.state = profile
        elif not self.state == profile:
            await self._event_builder(self.state, profile)
            self.state = profile

    async def _event_builder(self, previousState, currentState):
        if not previousState.followingCount == currentState.followingCount:
            event = FollowingCountChange(
                self.user,
                currentState,
                previousState.followingCount,
                currentState.followingCount,
            )
            await self.watcher.eventQueue.put(event)
        if not previousState.followerCount == currentState.followerCount:
            event = FollowerCountChange(
                self.user,
                currentState,
                previousState.followerCount,
                currentState.followerCount,
            )
            await self.watcher.eventQueue.put(event)
        if not previousState.answerCount == currentState.answerCount:
            event = AnswerCountChange(
                self.user,
                currentState,
                previousState.answerCount,
                currentState.answerCount,
            )
            await self.watcher.eventQueue.put(event)

    async def start(self):
        self.logger.info(f"Going to start updater for username {self.user.username}")
        while True:
            self.logger.debug("Updater is running")
            try:
                await self._update()
            except Exception as e:
                print(e, self.user.username)
            await asyncio.sleep(self.update_interval)
