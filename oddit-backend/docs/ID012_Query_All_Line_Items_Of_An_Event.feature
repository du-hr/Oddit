Feature: Query all line items for an event

As a SSMU club executive
I would like to visualize all line items for an event
So that I can check details of the line items of that event


Scenario Outline: Query all line items for an event by event id (Normal Flow)

Given a SSMU club executive is logged into the Oddit system
And the following line items for an event "Samosa Sale" with event_id 1 are created by the club
| line_item_id | line_item_name | projected_amount |  category  |
|      1       |     Soda       |        -20       | recreation |
|      2       |  Ticket Sale   |        +200      | recreation |
When the SSMU club executive requests the list of line items for the event  "Samosa Sale" by its event_id 1
Then all line items for the event with corresponding <line_item_name>, <projected_amount>, <category> and <note> are displayed
| line_item_id | line_item_name | projected_amount |  category  |
|      1       |     Soda       |        -20       | recreation |
|      2       |  Ticket Sale   |        +200      | recreation |

Scenario Outline: Query all line items for an event by event name (Alternative Flow)

Given a SSMU club executive is logged into the Oddit system
And the following line items for an event "Samosa Sale" are created by the club
| line_item_id | line_item_name | projected_amount |  category  |
|      1       |     Soda       |        -20       | recreation |
|      2       |  Ticket Sale   |        +200      | recreation |
When the SSMU club executive requests the list of line items for the event "Samosa Sale"
Then all line items for the event with corresponding <line_item_name>, <projected_amount>, <category> and <note> are displayed
| line_item_id | line_item_name | projected_amount |  category  |
|      1       |     Soda       |        -20       | recreation |
|      2       |  Ticket Sale   |        +200      | recreation |


Scenario Outline: Query list of line items of an event with an incorrect line item name (Error Flow)

Given a SSMU club executive is logged into the Oddit system
And there are line items created for events by the club
When requesting a list of line items for an invalid event
Then an error message "No event found" is issued
