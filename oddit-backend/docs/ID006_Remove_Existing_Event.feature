Feature: Remove existing event

As an executive of a SSMU club
I would like to delete an existing event
So that I can remove unuseful events and keep my event list organized.

Scenario: delete an existing event with an event id (Normal Flow)

Given user with a user id 2 is logged into the Oddit System
And the following events would be shown
| event_id | event_name     | event_date | user_id |
| 1        | Samosa Sale    | 10/1/20    |  3      |
| 2        | Speaker Series | 8/7/20     |  4      |
| 3        | Camping Trip   | 2/12/20    |  3      |
| 4        | Movie Night    | 11/15/20   |  2      |
When the user requests to remove the event with an event id 4
Then the following event list is returned
| event_id | event_name     | event_date | user_id |
| 1        | Samosa Sale    | 10/1/20    |  3      |
| 2        | Speaker Series | 8/7/20     |  4      |
| 3        | Camping Trip   | 2/12/20    |  3      |

Scenario: delete existing events with event ids (Alternative Flow)

Given user with a user id 3 is logged into the Oddit System
And the following events would be shown
| event_id | event_name     | event_date | user_id |
| 1        | Samosa Sale    | 10/1/20    |  3      |
| 2        | Speaker Series | 8/7/20     |  4      |
| 3        | Camping Trip   | 2/12/20    |  3      |
| 4        | Movie Night    | 11/15/20   |  2      |
When the user requests to remove the events with ids 1 and 3 
Then the following event list is returned
| event_id | event_name     | event_date | user_id |
| 2        | Speaker Series | 8/7/20     |  4      |
| 4        | Movie Night    | 11/15/20   |  2      |


Scenario: delete an existing event with an invalid event id (Error Flow)
Given user with a user id <user_id> is logged into the Oddit System
And the following events would be shown
| event_id | event_name     | event_date | user_id |
| 1        | Samosa Sale    | 10/1/20    |  3      |
| 2        | Speaker Series | 8/7/20     |  4      |
| 3        | Camping Trip   | 2/12/20    |  3      |
| 4        | Movie Night    | 11/15/20   |  2      |
When the user requests to remove an event with an invalid event id <event_id>
Then a error message "Event does not exist" is generated


