Feature: Query list of events by user

As a SSMU club executive
I would like to visualize the events associated with the club
So that I can check details of events


Scenario Outline: Query list of events (Normal Flow)

Given a SSMU club executive is logged into the Oddit system
And the following events are created by the club
| event_id |   event_name   | event_date |
|    1     |  Samosa Sale   | 10/1/20    |
|    2     |  Speaker Series| 8/7/20     |
|    3     |  Camping Trip  | 2/12/20    |
|    4     |  Movie Night   | 11/15/20   |
|    5     |  Laser Tag     | 9/8/20     |
When the SSMU club executive requests the list of events
Then all club events with corresponding <event_id>, <event_name> and <event_date> are displayed
| event_id |   event_name   | event_date |
|    4     |  Movie Night   | 11/15/20   |
|    1     |  Samosa Sale   | 10/1/20    |
|    5     |  Laser Tag     | 9/8/20     |
|    2     |  Speaker Series| 8/7/20     |
|    3     |  Camping Trip  | 2/12/20    |

Scenario Outline: Query list of events after canceling an event (Alternate Flow)

Given a SSMU club executive is logged into the Oddit system
And the following events are created by the club
| event_id|   event_name   | event_date |
|    1    |  Samosa Sale   | 10/1/20    |
|    2    |  Speaker Series| 8/7/20     |
|    3    |  Camping Trip  | 2/12/20    |
|    4    |  Movie Night   | 11/15/20   |
|    5    |  Laser Tag     | 9/8/20     |
And event "Laser Tag" is canceled
When the SSMU club executive requests the list of events
Then the updated list of events with corresponding <event_id>, <event_name> and <event_date> are displayed
| event_id |   event_name   | event_date |
|    4     |  Movie Night   | 11/15/20   |
|    1     |  Samosa Sale   | 10/1/20    |
|    2     |  Speaker Series| 8/7/20     |
|    3     |  Camping Trip  | 2/12/20    |

Scenario Outline: Query list of events with specified date range (Alternate Flow)

Given a SSMU club executive is logged into the Oddit system
And there are events created by the club
And a start date is specified
And an end date is specified
When requesting a list of events between the start date and end date
Then All events of the club within the specified date range are displayed


Scenario Outline: Query list of events with an invalid date (Error Flow)

Given a SSMU club executive is logged into the Oddit system
And there are events created by the club
And a start date is specified
And an end date is specified with invalid day or month or year
When requesting a list of events between the start date and end date
Then no event is displayed
And message "The end date is invalid" is issued

Scenario Outline: Query list of events with invalid range (Error Flow)

Given a SSMU club executive is logged into the Oddit system
And there are events created by the club
And a start date is specified
And an end date is specified
And the start date is later than then end date
When requesting a list of events between the start date and end date
Then no event is displayed
And message "Invalid date range" is issued
