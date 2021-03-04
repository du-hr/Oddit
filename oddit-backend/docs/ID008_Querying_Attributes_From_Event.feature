Feature: Request Attributes from an Event

As an executive SSMU employee
I would like to identify attributes from an event
So that I can review an event for planning


Scenario: Authorized club executive identifies attributes of an event by identification (Normal Flow)

Given club executive with a <user_id> is logged into the Oddit System
And the following events have been created

| event_id | event_name     | event_date | user_id |
| 1        | Samosa Sale    | 10/1/20    |  3      |
| 2        | Speaker Series | 8/7/20     |  4      |
| 3        | Camping Trip   | 2/12/20    |  3      |
| 4        | Movie Night    | 11/15/20   |  2      |
| 5        | Laser Tag      | 9/8/20     |  1      |

When the club executive requests attributes from event_id: 4
Then the following attributes are displayed
| event_id | event_name     | event_date | user_id |
| 4        | Movie Night    | 11/15/20   |  2      |


Scenario: Authorized club executive obtains attributes of an event by name (Alternate Flow)
Given club executive with <user_id> is logged into the Oddit System
And the following events have been created 
| event_id | event_name     | event_date | user_id |
| 1        | Samosa Sale    | 10/1/20    |  3      |
| 2        | Speaker Series | 8/7/20     |  4      |
| 3        | Camping Trip   | 2/12/20    |  3      |
| 4        | Movie Night    | 11/15/20   |  2      |
| 5        | Laser Tag      | 9/8/20     |  1      |

When the club executive requests attributes from event_name: Samosa Sale
Then the following attributes are displayed
| event_id | event_name     | event_date | user_id |
| 1        | Samosa Sale    | 10/1/20    |  3      |

Scenario: Authorized club executive obtains attributes of an event by event date (Alternate Flow)
Given club executive with <user_id> is logged into the Oddit System
And the following events have been created 
| event_id | event_name     | event_date | user_id |
| 1        | Samosa Sale    | 10/1/20    |  3      |
| 2        | Speaker Series | 8/7/20     |  4      |
| 3        | Camping Trip   | 2/12/20    |  3      |
| 4        | Movie Night    | 11/15/20   |  2      |
| 5        | Laser Tag      | 9/8/20     |  1      |

When the club executive requests attributes from event_date: 8/7/20
Then the following attributes are displayed
| event_id | event_name     | event_date | user_id |
| 2        | Speaker Series | 8/7/20     |  4      |

Scenario: Authorized club executive obtains attributes of an event by after deletion (Error Flow)
Given the club executive with <user_id> is logged into the Oddit System
And the following events have been created 
| event_id | event_name     | event_date | user_id |
| 1        | Samosa Sale    | 10/1/20    |  3      |
| 2        | Speaker Series | 8/7/20     |  4      |
| 3        | Camping Trip   | 2/12/20    |  3      |
| 4        | Movie Night    | 11/15/20   |  2      |
| 5        | Laser Tag      | 9/8/20     |  1      |
And event name: Camping Trip is deleted.
When the club executive with <user_id> requests attributes from event_name: Camping Trip
Then a message indicating Event does not exist is generated
