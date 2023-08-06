import pytest
from data_team_py_slack_notifier.data_team_py_slack_notifier import parse_event


@pytest.fixture
def mock_event_sns_success():
    event = {
        "Records": [
            {
                "EventSource": "aws:sns",
                "EventVersion": "1.0",
                "EventSubscriptionArn": "arn:aws:sns:eu-west-2:309161096106:glue-monitoring:8827e346-e2db-42f7-95f0-d66759181897",
                "Sns": {
                    "Type": "Notification",
                    "MessageId": "58fee2ac-7c63-5667-bd4e-bbf3af704c0f",
                    "TopicArn": "arn:aws:sns:eu-west-2:309161096106:glue-monitoring",
                    "Subject": None,
                    "Message": '{"version":"0","id":"e3b6465b-835f-a022-28cc-7524776f3395","detail-type":"Glue Job State Change","source":"aws.glue","account":"309161096106","time":"2021-07-07T16:05:36Z","region":"eu-west-2","resources":[],"detail":{"jobName":"DE-209-test","severity":"INFO","state":"SUCCEEDED","jobRunId":"jr_c4a93310af669b1fe899952ed184fe712ff5c471bab7a1c002f8784dc81be181","message":"Job run succeeded"}}',
                    "Timestamp": "2021-07-07T16:05:39.180Z",
                    "SignatureVersion": "1",
                    "Signature": "OzlczeD9GPBWpFCO6ikTJwBtwnCDxs2KtiVFVzZ77fMamD9mhnJxVFjrCKcx2DOtIUtYs6wGuBp07UCIMPs53Ak4yK3Bz4fRsQVq1YOoYRCODnlF1M7ye1zSvQj4y7eS3w1FncUu7sHw3vPnyqXxJ8w9aN61SUKha1FGDJZG46Deupno5mLcu81x9cmcPpThEiyj+kPigd9vu4QXaBs/7EzKlIeLtMOj8y7WtLoCYXev58WsYqnGeByCZB5xUhxwcmD0fhK6ofiin4aTCurIkhYMGbJ/52cIksJ69SAV9oFSgoUdPVauTLHe5MrLZyadsYn/cDV5gekWaOVq/vMU7w==",
                    "SigningCertUrl": "https://sns.eu-west-2.amazonaws.com/SimpleNotificationService-010a507c1833636cd94bdb98bd93083a.pem",
                    "UnsubscribeUrl": "https://sns.eu-west-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:eu-west-2:309161096106:glue-monitoring:8827e346-e2db-42f7-95f0-d66759181897",
                    "MessageAttributes": {},
                },
            }
        ]
    }
    context = None
    return event, context


def test_parse_event_sns_success(mock_event_sns_success):
    expected_result = (
        {"statusCode": 200, "body": "ok"},
        {
            "blocks": [
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": " _SERVICE_: aws.glue"},
                },
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": "_PROCESS_: DE-209-test"},
                },
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": "_TIME_: 2021-07-07T16:05:36Z"},
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "_JOB ID_: jr_c4a93310af669b1fe899952ed184fe712ff5c471bab7a1c002f8784dc81be181",
                    },
                },
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": "_STATE_: SUCCEEDED "},
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "_NOTIFICATION MESSAGE_: Job run succeeded",
                    },
                },
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": "--------------------"},
                },
            ]
        },
    )
    result = parse_event(*mock_event_sns_success)
    assert result == expected_result


@pytest.fixture
def mock_event_sns_failure():
    event = {
        "Records": [
            {
                "EventSource": "aws:sns",
                "EventVersion": "1.0",
                "EventSubscriptionArn": "arn:aws:sns:eu-west-2:309161096106:glue-monitoring:8827e346-e2db-42f7-95f0-d66759181897",
                "Sns": {
                    "Type": "Notification",
                    "MessageId": "58fee2ac-7c63-5667-bd4e-bbf3af704c0f",
                    "TopicArn": "arn:aws:sns:eu-west-2:309161096106:glue-monitoring",
                    "Subject": None,
                    "Message": '{"version":"0","id":"e3b6465b-835f-a022-28cc-7524776f3395","detail-type":"Glue Job State Change","source":"aws.glue","account":"309161096106","time":"2021-07-07T16:05:36Z","region":"eu-west-2","resources":[],"detail":{"jobName":"DE-209-test","severity":"INFO","state":"FAILED","jobRunId":"jr_c4a93310af669b1fe899952ed184fe712ff5c471bab7a1c002f8784dc81be181","message":"Job run has failed."}}',
                    "Timestamp": "2021-07-07T16:05:39.180Z",
                    "SignatureVersion": "1",
                    "Signature": "OzlczeD9GPBWpFCO6ikTJwBtwnCDxs2KtiVFVzZ77fMamD9mhnJxVFjrCKcx2DOtIUtYs6wGuBp07UCIMPs53Ak4yK3Bz4fRsQVq1YOoYRCODnlF1M7ye1zSvQj4y7eS3w1FncUu7sHw3vPnyqXxJ8w9aN61SUKha1FGDJZG46Deupno5mLcu81x9cmcPpThEiyj+kPigd9vu4QXaBs/7EzKlIeLtMOj8y7WtLoCYXev58WsYqnGeByCZB5xUhxwcmD0fhK6ofiin4aTCurIkhYMGbJ/52cIksJ69SAV9oFSgoUdPVauTLHe5MrLZyadsYn/cDV5gekWaOVq/vMU7w==",
                    "SigningCertUrl": "https://sns.eu-west-2.amazonaws.com/SimpleNotificationService-010a507c1833636cd94bdb98bd93083a.pem",
                    "UnsubscribeUrl": "https://sns.eu-west-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:eu-west-2:309161096106:glue-monitoring:8827e346-e2db-42f7-95f0-d66759181897",
                    "MessageAttributes": {},
                },
            }
        ]
    }
    context = None
    return event, context


def test_parse_event_sns_failure(mock_event_sns_failure):
    expected_result = (
        {"statusCode": 200, "body": "ok"},
        {
            "blocks": [
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": " _SERVICE_: aws.glue"},
                },
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": "_PROCESS_: DE-209-test"},
                },
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": "_TIME_: 2021-07-07T16:05:36Z"},
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "_JOB ID_: jr_c4a93310af669b1fe899952ed184fe712ff5c471bab7a1c002f8784dc81be181",
                    },
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "_STATE_:  :no_entry: *FAILED* :no_entry:  ",
                    },
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "_NOTIFICATION MESSAGE_: Job run has failed.",
                    },
                },
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": "--------------------"},
                },
            ]
        },
    )
    result = parse_event(*mock_event_sns_failure)
    assert result == expected_result


@pytest.fixture
def mock_event_custom_process_failure():
    event = {
        "source": "somesource",
        "time": "sometime",
        "detail": {
            "jobName": "somejob",
            "state": "some failed string",
            "message": "process has failed.",
        },
    }
    context = None
    return event, context


def test_parse_event_custom_failure(mock_event_custom_process_failure):
    expected_result = (
        {"statusCode": 200, "body": "ok"},
        {
            "blocks": [
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": " _SERVICE_: somesource"},
                },
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": "_PROCESS_: somejob"},
                },
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": "_TIME_: sometime"},
                },
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": "_JOB ID_: Untracked."},
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "_STATE_:  :no_entry: *some failed string* :no_entry:  ",
                    },
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "_NOTIFICATION MESSAGE_: process has failed.",
                    },
                },
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": "--------------------"},
                },
            ]
        },
    )
    result = parse_event(*mock_event_custom_process_failure)
    assert result == expected_result


@pytest.fixture
def mock_event_custom_process_key_error():
    event = {
        "unexpected_key_here": "somesource",
        "time": "sometime",
        "detail": {
            "jobName": "somejob",
            "state": "some failed string",
            "message": "process has failed.",
        },
    }
    context = None
    return event, context


def test_parse_event_custom_process_key_error(mock_event_custom_process_key_error):
    expected_result = (
        {"statusCode": 500, "error": "\"'source'\""},
        {
            "text": " :no_entry: *The slack notifier failed. Can`t tell anything about the process. Notifier has received an input key it can`t deal with.* :no_entry: . The event is {'unexpected_key_here': 'somesource', 'time': 'sometime', 'detail': {'jobName': 'somejob', 'state': 'some failed string', 'message': 'process has failed.'}}"
        },
    )
    result = parse_event(*mock_event_custom_process_key_error)
    assert result == expected_result


@pytest.fixture
def mock_event_sns_key_error_1():
    event = {
        "Records": [
            {
                "WrongKeyHere": "aws:sns",
                "EventVersion": "1.0",
                "EventSubscriptionArn": "arn:aws:sns:eu-west-2:309161096106:glue-monitoring:8827e346-e2db-42f7-95f0-d66759181897",
                "Sns": {
                    "Type": "Notification",
                    "MessageId": "58fee2ac-7c63-5667-bd4e-bbf3af704c0f",
                    "TopicArn": "arn:aws:sns:eu-west-2:309161096106:glue-monitoring",
                    "Subject": None,
                    "Message": '{"version":"0","id":"e3b6465b-835f-a022-28cc-7524776f3395","detail-type":"Glue Job State Change","source":"aws.glue","account":"309161096106","time":"2021-07-07T16:05:36Z","region":"eu-west-2","resources":[],"detail":{"jobName":"DE-209-test","severity":"INFO","state":"SUCCEEDED","jobRunId":"jr_c4a93310af669b1fe899952ed184fe712ff5c471bab7a1c002f8784dc81be181","message":"Job run succeeded"}}',
                    "Timestamp": "2021-07-07T16:05:39.180Z",
                    "SignatureVersion": "1",
                    "Signature": "OzlczeD9GPBWpFCO6ikTJwBtwnCDxs2KtiVFVzZ77fMamD9mhnJxVFjrCKcx2DOtIUtYs6wGuBp07UCIMPs53Ak4yK3Bz4fRsQVq1YOoYRCODnlF1M7ye1zSvQj4y7eS3w1FncUu7sHw3vPnyqXxJ8w9aN61SUKha1FGDJZG46Deupno5mLcu81x9cmcPpThEiyj+kPigd9vu4QXaBs/7EzKlIeLtMOj8y7WtLoCYXev58WsYqnGeByCZB5xUhxwcmD0fhK6ofiin4aTCurIkhYMGbJ/52cIksJ69SAV9oFSgoUdPVauTLHe5MrLZyadsYn/cDV5gekWaOVq/vMU7w==",
                    "SigningCertUrl": "https://sns.eu-west-2.amazonaws.com/SimpleNotificationService-010a507c1833636cd94bdb98bd93083a.pem",
                    "UnsubscribeUrl": "https://sns.eu-west-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:eu-west-2:309161096106:glue-monitoring:8827e346-e2db-42f7-95f0-d66759181897",
                    "MessageAttributes": {},
                },
            }
        ]
    }
    context = None
    return event, context


def test_parse_event_sns_key_error_1(mock_event_sns_key_error_1):
    expected_result = (
        {"statusCode": 500, "error": "\"'source'\""},
        {
            "text": " :no_entry: *The slack notifier failed. Can`t tell anything about the process. Notifier has received an input key it can`t deal with.* :no_entry: . The event is {'Records': [{'WrongKeyHere': 'aws:sns', 'EventVersion': '1.0', 'EventSubscriptionArn': 'arn:aws:sns:eu-west-2:309161096106:glue-monitoring:8827e346-e2db-42f7-95f0-d66759181897', 'Sns': {'Type': 'Notification', 'MessageId': '58fee2ac-7c63-5667-bd4e-bbf3af704c0f', 'TopicArn': 'arn:aws:sns:eu-west-2:309161096106:glue-monitoring', 'Subject': None, 'Message': '{\"version\":\"0\",\"id\":\"e3b6465b-835f-a022-28cc-7524776f3395\",\"detail-type\":\"Glue Job State Change\",\"source\":\"aws.glue\",\"account\":\"309161096106\",\"time\":\"2021-07-07T16:05:36Z\",\"region\":\"eu-west-2\",\"resources\":[],\"detail\":{\"jobName\":\"DE-209-test\",\"severity\":\"INFO\",\"state\":\"SUCCEEDED\",\"jobRunId\":\"jr_c4a93310af669b1fe899952ed184fe712ff5c471bab7a1c002f8784dc81be181\",\"message\":\"Job run succeeded\"}}', 'Timestamp': '2021-07-07T16:05:39.180Z', 'SignatureVersion': '1', 'Signature': 'OzlczeD9GPBWpFCO6ikTJwBtwnCDxs2KtiVFVzZ77fMamD9mhnJxVFjrCKcx2DOtIUtYs6wGuBp07UCIMPs53Ak4yK3Bz4fRsQVq1YOoYRCODnlF1M7ye1zSvQj4y7eS3w1FncUu7sHw3vPnyqXxJ8w9aN61SUKha1FGDJZG46Deupno5mLcu81x9cmcPpThEiyj+kPigd9vu4QXaBs/7EzKlIeLtMOj8y7WtLoCYXev58WsYqnGeByCZB5xUhxwcmD0fhK6ofiin4aTCurIkhYMGbJ/52cIksJ69SAV9oFSgoUdPVauTLHe5MrLZyadsYn/cDV5gekWaOVq/vMU7w==', 'SigningCertUrl': 'https://sns.eu-west-2.amazonaws.com/SimpleNotificationService-010a507c1833636cd94bdb98bd93083a.pem', 'UnsubscribeUrl': 'https://sns.eu-west-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:eu-west-2:309161096106:glue-monitoring:8827e346-e2db-42f7-95f0-d66759181897', 'MessageAttributes': {}}}]}"
        },
    )
    result = parse_event(*mock_event_sns_key_error_1)
    assert result == expected_result


@pytest.fixture
def mock_event_sns_key_error_2():
    event = {
        "Records": [
            {
                "EventSource": "aws:sns",
                "EventVersion": "1.0",
                "EventSubscriptionArn": "arn:aws:sns:eu-west-2:309161096106:glue-monitoring:8827e346-e2db-42f7-95f0-d66759181897",
                "Sns": {
                    "Type": "Notification",
                    "MessageId": "58fee2ac-7c63-5667-bd4e-bbf3af704c0f",
                    "TopicArn": "arn:aws:sns:eu-west-2:309161096106:glue-monitoring",
                    "Subject": None,
                    "Message": '{"version":"0","id":"e3b6465b-835f-a022-28cc-7524776f3395","detail-type":"Glue Job State Change","source":"aws.glue","account":"309161096106","WRONGKEYHERE":"2021-07-07T16:05:36Z","region":"eu-west-2","resources":[],"detail":{"jobName":"DE-209-test","severity":"INFO","state":"SUCCEEDED","jobRunId":"jr_c4a93310af669b1fe899952ed184fe712ff5c471bab7a1c002f8784dc81be181","message":"Job run succeeded"}}',
                    "Timestamp": "2021-07-07T16:05:39.180Z",
                    "SignatureVersion": "1",
                    "Signature": "OzlczeD9GPBWpFCO6ikTJwBtwnCDxs2KtiVFVzZ77fMamD9mhnJxVFjrCKcx2DOtIUtYs6wGuBp07UCIMPs53Ak4yK3Bz4fRsQVq1YOoYRCODnlF1M7ye1zSvQj4y7eS3w1FncUu7sHw3vPnyqXxJ8w9aN61SUKha1FGDJZG46Deupno5mLcu81x9cmcPpThEiyj+kPigd9vu4QXaBs/7EzKlIeLtMOj8y7WtLoCYXev58WsYqnGeByCZB5xUhxwcmD0fhK6ofiin4aTCurIkhYMGbJ/52cIksJ69SAV9oFSgoUdPVauTLHe5MrLZyadsYn/cDV5gekWaOVq/vMU7w==",
                    "SigningCertUrl": "https://sns.eu-west-2.amazonaws.com/SimpleNotificationService-010a507c1833636cd94bdb98bd93083a.pem",
                    "UnsubscribeUrl": "https://sns.eu-west-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:eu-west-2:309161096106:glue-monitoring:8827e346-e2db-42f7-95f0-d66759181897",
                    "MessageAttributes": {},
                },
            }
        ]
    }
    context = None
    return event, context


def test_parse_event_sns_key_error_2(mock_event_sns_key_error_2):
    expected_result = (
        {"statusCode": 500, "error": "\"'time'\""},
        {
            "text": " :no_entry: *The slack notifier failed. Can`t tell anything about the process. Notifier has received an input key it can`t deal with.* :no_entry: . The event is {'Records': [{'EventSource': 'aws:sns', 'EventVersion': '1.0', 'EventSubscriptionArn': 'arn:aws:sns:eu-west-2:309161096106:glue-monitoring:8827e346-e2db-42f7-95f0-d66759181897', 'Sns': {'Type': 'Notification', 'MessageId': '58fee2ac-7c63-5667-bd4e-bbf3af704c0f', 'TopicArn': 'arn:aws:sns:eu-west-2:309161096106:glue-monitoring', 'Subject': None, 'Message': '{\"version\":\"0\",\"id\":\"e3b6465b-835f-a022-28cc-7524776f3395\",\"detail-type\":\"Glue Job State Change\",\"source\":\"aws.glue\",\"account\":\"309161096106\",\"WRONGKEYHERE\":\"2021-07-07T16:05:36Z\",\"region\":\"eu-west-2\",\"resources\":[],\"detail\":{\"jobName\":\"DE-209-test\",\"severity\":\"INFO\",\"state\":\"SUCCEEDED\",\"jobRunId\":\"jr_c4a93310af669b1fe899952ed184fe712ff5c471bab7a1c002f8784dc81be181\",\"message\":\"Job run succeeded\"}}', 'Timestamp': '2021-07-07T16:05:39.180Z', 'SignatureVersion': '1', 'Signature': 'OzlczeD9GPBWpFCO6ikTJwBtwnCDxs2KtiVFVzZ77fMamD9mhnJxVFjrCKcx2DOtIUtYs6wGuBp07UCIMPs53Ak4yK3Bz4fRsQVq1YOoYRCODnlF1M7ye1zSvQj4y7eS3w1FncUu7sHw3vPnyqXxJ8w9aN61SUKha1FGDJZG46Deupno5mLcu81x9cmcPpThEiyj+kPigd9vu4QXaBs/7EzKlIeLtMOj8y7WtLoCYXev58WsYqnGeByCZB5xUhxwcmD0fhK6ofiin4aTCurIkhYMGbJ/52cIksJ69SAV9oFSgoUdPVauTLHe5MrLZyadsYn/cDV5gekWaOVq/vMU7w==', 'SigningCertUrl': 'https://sns.eu-west-2.amazonaws.com/SimpleNotificationService-010a507c1833636cd94bdb98bd93083a.pem', 'UnsubscribeUrl': 'https://sns.eu-west-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:eu-west-2:309161096106:glue-monitoring:8827e346-e2db-42f7-95f0-d66759181897', 'MessageAttributes': {}}}]}"
        },
    )
    result = parse_event(*mock_event_sns_key_error_2)
    print("Result is", result)
    assert result == expected_result
