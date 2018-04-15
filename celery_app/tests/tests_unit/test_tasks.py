from unittest.mock import patch

from celery.exceptions import Retry
from pytest import raises

from app.service import ServiceError
from app.tasks import do_task, TaskError


@patch('app.tasks.geoprocess')
def test_do_task_success(mock_add):
    # Act
    do_task(2, 3)

    # Assert
    mock_add.assert_called_with(2, 3)


@patch('app.tasks.geoprocess')
@patch('app.tasks.do_task.retry')
def test_do_task_handles_serviceerror_with_retry(mock_add_task_retry, mock_geoprocess):

    # Arrange
    mock_add_task_retry.side_effect = Retry()
    mock_geoprocess.side_effect = ServiceError('Random fail!')

    # Act/assert
    with raises(Retry):
        do_task(2, 1)


@patch('app.tasks.geoprocess')
@patch('app.tasks.do_task.retry')
def test_do_task_handles_unexpected_exception(mock_add_task_retry, mock_geoprocess):

    # Arrange
    mock_add_task_retry.side_effect = Retry()
    mock_geoprocess.side_effect = NotADirectoryError('Random fail!')

    # Act/assert
    with raises(TaskError):
        do_task(2, 1)
