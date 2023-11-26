"""
This module contains tests for the `application` module in the cognosis project.
It includes tests that verify the functionality of the application components, ensuring they perform as expected.
"""

import pytest
from cognosis.application import broker
from cognosis.FSK_mono.mono import UUID
from faststream.kafka import TestKafkaBroker
