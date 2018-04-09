from pytest import raises
from unittest.mock import patch

from celery.exceptions import Retry

from app.tasks import do_task_task


@patch('app.tasks.add')
def test_do_task_task_success(mock_add):
    # Act
    do_task_task(2, 3)

    # Assert
    mock_add.assert_called_with(2, 3)


@patch('app.tasks.add')
@patch('app.tasks.add_task.retry')
def test_do_task_task_handles_failure(mock_add_task_retry, mock_add):

    # Arrange
    mock_add_task_retry.side_effect = Retry()
    mock_add.side_effect = NotImplementedError('Random fail!')

    # Act/assert
    with raises(Retry):
        do_task_task(2, 1)
