Feature: Query attributes of line item

As an executive of a SSMU club
I would like to identify the attributes of a line item from an event
So that I can review the line item for budget planning

Scenario: Query attributes of a line item for an event by line item id (Normal Flow)

Given club executive is logged into the Oddit System
And the following line items have been created for a given event
| line_item_id | line_item_name | projected_amount | category   |
|      1       |     Soda       |       -20        |   Food     |
|      2       |  Ticket Sale   |      +200        | Recreation |
When the club executive requests attributes from line_item_id: 2
Then the following attributes are displayed
| line_item_id | line_item_name | projected_amount | category   |
|      2      |  Ticket Sale   |      +200        | Recreation |

Scenario: Query attributes of a line item for an event by line item name (Alternate Flow)

Given club executive is logged into the Oddit System
And the following line items have been created for a given event
| line_item_id | line_item_name | projected_amount | category   |
| 	   1       |      Soda      |       -20        |   Food     |
|	     2       |  Ticket Sale   |      +200        | Recreation |
When the club executive requests attributes from line_item_name "Soda"
Then the following attributes are displayed
| line_item_id | line_item_name | projected_amount | category   |
|      1       |      Soda      | -20              |   Food     |

Scenario: Query attributes of a line item for an event after its deletion (Error Flow)

Given club executive is logged into the Oddit System
And the following line items have been created for a given event
| line_item_id | line_item_name | projected_amount | category   |
| 	   1       | 	 Soda         |       -20        |   Food     |
|      2       |  Ticket Sale   |      +200        | Recreation |
And line item with name "Soda" is deleted
When the club executive requests attributes from line_item_name: Soda
Then an error message indicating line item does not exist is generated
