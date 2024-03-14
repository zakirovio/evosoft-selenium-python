from config import settings

domain = "https://x.com/elonmusk/"

login = settings.T_USERNAME
password = settings.T_PASSWORD

public_token = "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
my_valid_guest_token = "1768275043996315930"
elon_params = {
        'variables': '{"userId":"44196397","count":10,"includePromotedContent":false,"withQuickPromoteEligibilityTweetFields":false,"withVoice":false,"withV2Timeline":true}',
        'features': '{"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"c9s_tweet_anatomy_moderator_badge_enabled":true,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}',
    }
#  Bearer постоянен? проверял на разных браузерах и в режиме инкогнито, везде одинаковый
headers = {
        'authority': 'api.twitter.com',
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'authorization': f'{public_token}',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://twitter.com',
        'pragma': 'no-cache',
        'referer': 'https://twitter.com/',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'x-client-transaction-id': 'M+/tFbufD327j2MTnNSOk3PmxkBfA2aBOMZNS1nNoUhwU+FsZv3EQy3PoGbA9UWKRitCkDJHUfJzCww/eUtD984+oSB1Mg',
        'x-guest-token': '',
        'x-twitter-active-user': 'yes',
        'x-twitter-client-language': 'ru',
    }

common = {
    'authority': 'twitter.com',
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'referer': 'https://twitter.com/i/flow/login',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'script',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
}

flow_data = {
    'input_flow_data': {
        'flow_context': {
            'debug_overrides': {},
            'start_location': {
                'location': 'manual_link',
            },
        },
    },
    'subtask_versions': {
        'action_list': 2,
        'alert_dialog': 1,
        'app_download_cta': 1,
        'check_logged_in_account': 1,
        'choice_selection': 3,
        'contacts_live_sync_permission_prompt': 0,
        'cta': 7,
        'email_verification': 2,
        'end_flow': 1,
        'enter_date': 1,
        'enter_email': 2,
        'enter_password': 5,
        'enter_phone': 2,
        'enter_recaptcha': 1,
        'enter_text': 5,
        'enter_username': 2,
        'generic_urt': 3,
        'in_app_notification': 1,
        'interest_picker': 3,
        'js_instrumentation': 1,
        'menu_dialog': 1,
        'notifications_permission_prompt': 2,
        'open_account': 2,
        'open_home_timeline': 1,
        'open_link': 1,
        'phone_verification': 4,
        'privacy_options': 1,
        'security_key': 3,
        'select_avatar': 4,
        'select_banner': 2,
        'settings_list': 7,
        'show_code': 1,
        'sign_up': 2,
        'sign_up_review': 4,
        'tweet_selection_urt': 1,
        'update_users': 1,
        'upload_media': 1,
        'user_recommendations_list': 4,
        'user_recommendations_urt': 1,
        'wait_spinner': 3,
        'web_modal': 1,
    },
}

json_data = {
    'flow_token': '',
    'subtask_inputs': [
        {
            'subtask_id': 'LoginJsInstrumentationSubtask',
            'js_instrumentation': {
                'response': '{"rf":{"a54cd41635ee18052ac2c49e0233023f47ffbcc807bea5a4377f328bca01de9a":-19,"d17cb96929fcdfc52b643ba747151f255100e9b5515bc9e7779a20a76ece4e02":-8,"a2e8c94cf38c8478b72ea8f8753b4a375db4f28175f172ded7465556ae9f0479":12,"b660f03faf32f328b2d7e21e04e2a36e3574c23cc08665fdd218f35be6021754":-37},"s":"dSQzOKY3OS5OkT9DwSk4GZ4ILjmEeyKMtjgZmualHufJzigy27YF-H6SR-pekISOP5ETLf7J5G_LaZTtItbpatUPpPJBeSOMiC8qvFU8T4bcPad9zYFF5RXzQqzEMmmrXOxKJ-LH8v5bpq71_IceoMwcGGV-UFZ8wiI4MLvOVsZxA3X7YPweR2uqP6RPrgUkfmbL9PbRAqs0nbUnErbFm6FjkKvsdIB5i2ReCuwISvWYaRqtQ4VQuM-GsEE6yMBY_5gvoLpCsMA_sK_ladX8Hy75mHYKngqjlPzGCg7puEvHTdJDuIIRqda7g6f5DaTWlmok81tmNYpMWGMSrRHnDQAAAY485qOm"}',
                'link': 'next_link',
            },
        },
    ],
}

login_data = {
    'flow_token': '',
    'subtask_inputs': [
        {
            'subtask_id': 'LoginEnterUserIdentifierSSO',
            'settings_list': {
                'setting_responses': [
                    {
                        'key': 'user_identifier',
                        'response_data': {
                            'text_data': {
                                'result': f'{login}',
                            },
                        },
                    },
                ],
                'link': 'next_link',
            },
        },
    ],
}

password_data = {
    'flow_token': '',
    'subtask_inputs': [
        {
            'subtask_id': 'LoginEnterPassword',
            'enter_password': {
                'password': f'{password}',
                'link': 'next_link',
            },
        },
    ],
}

check_data = {
    'flow_token': '',
    'subtask_inputs': [
        {
            'subtask_id': 'AccountDuplicationCheck',
            'check_logged_in_account': {
                'link': 'AccountDuplicationCheck_false',
            },
        },
    ],
}

csrf_change_data = {
    'variables': '{"withCommunitiesMemberships":true}',
    'features': '{"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"responsive_web_graphql_timeline_navigation_enabled":true}',
    'fieldToggles': '{"isDelegate":false,"withAuxiliaryUserLabels":false}',
}

# 2-factor auth
confirm_data = {
    'flow_token': '',
    'subtask_inputs': [
        {
            'subtask_id': 'LoginAcid',
            'enter_text': {
                'text': '',
                'link': 'next_link',
            },
        },
    ],
}
