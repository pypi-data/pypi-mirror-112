from cartesio.model.callback import CallbackABC

import logging


class CallbackLogging(CallbackABC):
    def __init__(self, logger):
        self.logger = logger

    def _callback(self, e_name, e_content):
        if e_name == 'on_generation_end':
            if e_content['flag'] == 'success':
                self.logger.info('generation successfully done')
            elif e_content['flag'] == 'fail':
                self.logger.error('generation failled')


def main():
    logger = logging.getLogger('create callback example')
    logging.basicConfig(level=logging.INFO)
    callback = CallbackLogging(logger)

    event_1 = {'name': 'on_generation_start', 'content': {'flag': 'success'}}
    event_2 = {'name': 'on_generation_end', 'content': {'flag': 'fail'}}

    event_3 = {'name': 'on_generation_start', 'content': {'flag': 'success'}}
    event_4 = {'name': 'on_generation_end', 'content': {'flag': 'success'}}

    callback.update(event_1)
    callback.update(event_2)
    callback.update(event_3)
    callback.update(event_4)


if __name__ == "__main__":
    main()
