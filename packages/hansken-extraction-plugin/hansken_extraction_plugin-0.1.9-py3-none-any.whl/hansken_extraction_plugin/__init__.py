"""
Copyright 2021 Netherlands Forensic Institute

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import sys

import logbook  # type: ignore
from logbook import compat, StreamHandler


# Log to stdout
log_handler = StreamHandler(sys.stdout, level='WARNING', bubble=True)
log_handler.push_application()

# redirect all calls to logging to logbook
compat.redirect_logging()

logbook.set_datetime_format('utc')
