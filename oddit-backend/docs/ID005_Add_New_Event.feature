Feature: Add Event
​
As an executive of a SSMU club
I would like to create an event
So that I can plan the budget for a future event or log the spendings for a past event
​
Scenario Outline: Add a New Event (Normal Flow)
 ​
Given user with a user id <user_id> is logged into the Oddit System
And <event_name> is the name of the event
And <event_date> is the start date of the event (date format ISO)
When requesting addition of a new event
Then a new event with a unique <event_id> is generated

| event_id | user_id | event_name     | event_date       |
| 1        | 3       | Samosa Sale    | 2020/03/01       |          
| 2        | 5       | Speaker Series | 2020/12/07       |
| 3        | 5       | Camping Trip   | 1987/12/31       |
| 4        | 7       | Movie Night    | 2030/07/07       |
| 5        | 9       | Laser Tag      | 2019/04/28       |
​
Scenario Outline: Attempt of creating an event without a name (Error Flow)

Given John Doe is logged into the Oddit system
When John Doe is trying to create an event without entering a name
Then an "Invalid Name" message is issued

Scenario Outline: Attempt of creating an event without a date (Error Flow)

Given John Doe is logged into the Oddit system
When John Doe is trying to create an event without entering a date
Then an "Invalid Date" message is issued

Scenario Outline: Attempt of creating an existing event (Error Flow)

Given Jane Doe is logged into the Oddit system
When Jane Doe is trying to create an event that has the same name and date with an event in the Oddit System
Then an "Event already submitted" message is issued

Scenario Outline: A user who is not logged into the Oddit system attempts to create an event (Error Flow)

Given Jane Doe is not logged into Oddit system
When Jane Doe is trying to create an event with user_id INVALID_USER_ID
Then an "Invalid User" message is issued
