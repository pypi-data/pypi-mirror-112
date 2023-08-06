# Copyright © 2021 Center of Research & Development <info@crnd.pro>

#######################################################################
# This Source Code Form is subject to the terms of the Mozilla Public #
# License, v. 2.0. If a copy of the MPL was not distributed with this #
# file, You can obtain one at http://mozilla.org/MPL/2.0/.            #
#######################################################################


def retry_iter(interval_timeout=0.5, max_retries=3, first_timeout=True):
    """ Retry as iterator - simple function that could be used as iterator to
        provide *retry* mechanism.

        :param float interval_timeout: timout to sleep between retries
        :param int max_retries: Number of retries before end of loop
        :param bool first_timeout: Do we need timeout before first iteration

        Example of usage::

            state = False
            for attempt in retry_iter(max_retries=5):
                if do_operation(params):
                    state = True
                    break
            if not state:
                raise Exception("Operation failed")
    """
    import time
    attempt = 0
    enable_timeout = first_timeout
    retry_timeout = interval_timeout

    while attempt < max_retries:
        attempt += 1

        if enable_timeout:
            time.sleep(retry_timeout)

        # Do work
        yield attempt

        enable_timeout = True


async def a_retry_iter(interval_timeout=0.5,
                       max_retries=3,
                       first_timeout=True):
    """ Async version of ``retry_iter`` function.

        :param float interval_timeout: timout to sleep between retries
        :param int max_retries: Number of retries before end of loop
        :param bool first_timeout: Do we need timeout before first iteration

        Example of usage::
            state = False
            async for attempt in a_retry_iter(max_retries=5):
                if await do_operation(params):
                    state = True
                    break
            if not state:
                raise Exception("Operation failed")
    """
    import asyncio
    attempt = 0
    enable_timeout = first_timeout
    retry_timeout = interval_timeout

    while attempt < max_retries:
        attempt += 1

        if enable_timeout:
            await asyncio.sleep(retry_timeout)

        # Do work
        yield attempt

        enable_timeout = True
