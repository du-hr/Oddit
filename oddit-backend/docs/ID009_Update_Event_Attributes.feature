Feature: Update event attributes

As an executive of a SSMU club
I would like to update an existing event
So that I can edit the info of an existing event and keep my event list up-to-date.

Scenario: Update an existing event using event id (Normal Flow)

Given user with a user id <user_id> is logged into the Oddit System
And the following events would be shown
| event_id | event_name     | event_date | user_id |
| 1        | Samosa Sale    | 10/1/20    |  3      |
| 2        | Speaker Series | 8/7/20     |  4      |
| 3        | Camping Trip   | 2/12/20    |  3      |
| 4        | Movie Night    | 11/15/20   |  2      |
When the user requests to update an existing event with event id 1 with new event name Samosa Bake Sale and new event date 11/1/20
Then the following event list is returned
| event_id | event_name       | event_date | user_id |
| 1        | Samosa Bake Sale | 11/1/20    |  3      |
| 2        | Speaker Series   | 8/7/20     |  4      |
| 3        | Camping Trip     | 2/12/20    |  3      |
| 4        | Movie Night      | 11/15/20   |  2      |

Scenario: Update an existing event name using event id (Alternate Flow)

Given user with a user id <user_id> is logged into the Oddit System
And the following events would be shown
| event_id | event_name     | event_date | user_id |
| 1        | Samosa Sale    | 10/1/20    |  3      |
| 2        | Speaker Series | 8/7/20     |  4      |
| 3        | Camping Trip   | 2/12/20    |  3      |
| 4        | Movie Night    | 11/15/20   |  2      |
When the user requests to update an existing event with event id 1 with new event name Samosa Bake Sale
Then the following event list is returneds
| event_id | event_name       | event_date | user_id |
| 1        | Samosa Bake Sale | 10/1/20    |  3      |
| 2        | Speaker Series   | 8/7/20     |  4      |
| 3        | Camping Trip     | 2/12/20    |  3      |
| 4        | Movie Night      | 11/15/20   |  2      |


Scenario: Update an existing event using invalid event id (Error Flow)

Given user with a user id <user_id> is logged into the Oddit System
And the following events would be shown
| event_id | event_name     | event_date | user_id |
| 1        | Samosa Sale    | 10/1/20    |  3      |
| 2        | Speaker Series | 8/7/20     |  4      |
| 3        | Camping Trip   | 2/12/20    |  3      |
| 4        | Movie Night    | 11/15/20   |  2      |
When the user requests to update an event with an event id 0
Then a error message "Event does not exist" is generated

Scenario Outline: A user who is not logged into the Oddit system attempts to update an event (Error Flow)

Given Jane Doe is not logged into the Oddit system
When Jane Doe is trying to update an event with user_id INVALID_USER_ID
Then an "Invalid User" message is issued
