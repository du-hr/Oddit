Feature: Remove line item to existing event

As an executive of a SSMU club
I would like to remove a line item from an existing event
So that I can have an estimated event budget

Scenario: Remove line item associated with an existing event (Normal Flow)
  
Given the executive is logged into the Oddit System
And the following events have been created
| event_id | event_name     | event_date | user_id | 
| 1        | Samosa Sale    | 10/1/20    | 3       | 
| 2        | Speaker Series | 8/7/20     | 4       | 
| 3        | Camping Trip   | 2/12/20    | 3       | 
| 4        | Movie Night    | 11/15/20   | 2       | 
And the executive selects an event with id 2
And the following table with line items is returned
| line_item_id | line_item_name | projected_amount | category    |
| 1            | Soda           | -20              | Food        | 
| 2            | Ticket Sale    | +200             | Recreation  |
| 3            | Fruit          | -50              | Food        |
| 4            | TV Equipment   | -150             | TV and AV   | 
| 5            | Sponsor A      | +500             | Sponsorship |
When the executive requests to remove the line item with id 3
Then the following line item table is returned
| line_item_id | line_item_name | projected_amount | category    |
| 1            | Soda           | -20              | Food        | 
| 2            | Ticket Sale    | +200             | Recreation  |
| 4            | TV Equipment   | -150             | TV and AV   | 
| 5            | Sponsor A      | +500             | Sponsorship | 


Scenario Outline: Remove multiple line items associated with an existing event (Alternate Flow)
  
Given the executive is logged into the Oddit System
And the following events have been created
| event_id | event_name     | event_date | user_id | 
| 1        | Samosa Sale    | 10/1/20    | 3       | 
| 2        | Speaker Series | 8/7/20     | 4       | 
| 3        | Camping Trip   | 2/12/20    | 3       | 
| 4        | Movie Night    | 11/15/20   | 2       | 
And the executive selects an event with id 2
And the following table with line items is returned
| line_item_id | line_item_name | projected_amount | category    | 
| 1            | Soda           | -20              | Food        | 
| 2            | Ticket Sale    | +200             | Recreation  | 
| 3            | Fruit          | -50              | Food        | 
| 4            | TV Equipment   | -150             | TV and AV   |
| 5            | Sponsor A      | +500             | Sponsorship |
When the executive requests to remove multiple line items with line item ids 1 and 3
Then line item "Soda" and "Fruit" are deleted
| line_item_id | line_item_name | projected_amount | category    |
| 2            | Ticket Sale    | +200             | Recreation  | 
| 4            | TV Equipment   | -150             | TV and AV   | 
| 5            | Sponsor A      | +500             | Sponsorship | 

Scenario Outline: Remove line item by id that does not exist (Error Flow)
  
Given the executive is logged into the Oddit System
And the following events have been created
| event_id | event_name     | event_date | user_id | 
| 1        | Samosa Sale    | 10/1/20    | 3       | 
| 2        | Speaker Series | 8/7/20     | 4       | 
| 3        | Camping Trip   | 2/12/20    | 3       | 
| 4        | Movie Night    | 11/15/20   | 2       | 
And the executive selects an event with id 2
And the following table with line items is returned
| line_item_id | line_item_name | projected_amount | category    | 
| 1            | Soda           | -20              | Food        | 
| 2            | Ticket Sale    | +200             | Recreation  |
| 3            | Fruit          | -50              | Food        |
| 4            | TV Equipment   | -150             | TV and AV   |
| 5            | Sponsor A      | +500             | Sponsorship |
When the executive requests to remove the line item with line item id 0
Then the an error message "Line Item Does not exist with this Identifier!" is returned
  
  
  
  
